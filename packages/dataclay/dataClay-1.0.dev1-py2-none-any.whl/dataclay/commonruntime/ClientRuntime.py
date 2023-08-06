"""Initialization and finalization of dataClay client API.

The `init` and `finish` functions are availble through the
dataclay.api package.
"""

import logging
import random
import time

from grpc import RpcError
from dataclay.commonruntime.Settings import settings
from dataclay.communication.grpc.clients.ExecutionEnvGrpcClient import EEClient
from dataclay.communication.grpc.clients.LogicModuleGrpcClient import LMClient
from dataclay.communication.grpc.messages.common.common_messages_pb2 import LANG_PYTHON
from dataclay.exceptions.exceptions import DataClayException
from dataclay.serialization.lib.DeserializationLibUtils import deserialize_return
from dataclay.serialization.lib.SerializationLibUtils import serialize_params_or_return
from dataclay.commonruntime.DataClayRuntime import DataClayRuntime
from dataclay.commonruntime.RuntimeType import RuntimeType
from dataclay.heap.ClientHeapManager import ClientHeapManager
from dataclay.loader.ClientObjectLoader import ClientObjectLoader

# Sentinel-like object to catch some typical mistakes
UNDEFINED_LOCAL = object()


class ClientRuntime(DataClayRuntime):
    
    current_type = RuntimeType.client

    def __init__(self):
        
        DataClayRuntime.__init__(self)
        
    def initialize_runtime_aux(self):
        self.dataclay_heap_manager = ClientHeapManager(self)
        self.dataclay_object_loader = ClientObjectLoader(self)
        
    def is_exec_env(self):
        return False

    def store_object(self, instance):
        raise RuntimeError("StoreObject can only be used from the ExecutionEnvironment")
    
    def choose_location(self, instance):
        """ Choose execution/make persistent location. 
        :param instance: Instance to use in call
        :returns: Location 
        :type instance: DataClayObject
        :rtype: DataClayID 
        """
        # // === DEFAULT EXECUTION LOCATION === //CURRENTLY NOT SUPPORTED 
        # ToDo: remove in java (dgasull)
        # // === HASHCODE EXECUTION LOCATION === //
        # ToDO: hashcode exec. loc 
        # get random
        exeenv_id = random.choice(list(self.get_execution_environments_info()))
        self.logger.verbose("ExecutionEnvironmentID obtained for execution = %s", exeenv_id)
        return exeenv_id
    
    def make_persistent(self, instance, alias, backend_id, recursive):
        """ This method creates a new Persistent Object using the provided stub
        instance and, if indicated, all its associated objects also Logic module API used for communication
        This function is called from a stub/execution class
        :param instance: Instance to make persistent
        :param backend_id: Indicates which is the destination backend
        :param recursive: Indicates if make persistent is recursive
        :param alias: Alias for the object
        :returns: ID of the backend in which te object was persisted.
        :type instance: DataClayObject
        :type backend_id: DataClayID
        :type recursive: boolean
        :type alias: string
        :rtype: DataClayID
        :raises RuntimeError: if backend id is UNDEFINED_LOCAL.
        """
        self.logger.debug("Starting make persistent object for instance %s with id %s", instance,
                     instance.get_object_id())
        if backend_id is UNDEFINED_LOCAL:
            # This is a commonruntime end user pitfall,
            # @abarcelo thinks that it is nice
            # (and exceptionally detailed) error
            raise RuntimeError("""
                You are trying to use dataclay.api.LOCAL but either:
                  - dataClay has not been initialized properly
                  - LOCAL has been wrongly imported.
                
                Be sure to use LOCAL with:
                
                from dataclay import api
                
                and reference it with `api.LOCAL`
                
                Refusing the temptation to guess.""")
        location = instance.get_hint()
        if location is None:
            location = backend_id
            # Choose location if needed
            # If object is already persistent -> it must have a Hint (location = hint here)
            # If object is not persistent -> location is choosen (provided backend id or random, hash...).
            if location is None:
                location = self.choose_location(instance)
            
        if not instance.is_persistent():

            # === MAKE PERSISTENT === #
            
            # set the default master location
            instance.set_master_location(location)
            # We serialize objects like volatile parameters
            parameters = list()
            parameters.append(instance)
            params_order = list()
            params_order.append("object")
            params_spec = dict()
            params_spec["object"] = "DataClayObject"  # not used, see serialized_params_or_return
            serialized_objs = serialize_params_or_return(
                params=parameters,
                iface_bitmaps=None,
                params_spec=params_spec,
                params_order=params_order,
                hint_volatiles=location,
                runtime=self,
                recursive=recursive)
            
            # Avoid some race-conditions in communication (make persistent + execute where
            # execute arrives before).
            self.add_volatiles_under_deserialization(serialized_objs[3])
            
            # Get EE
            try:
                execution_client = self.ready_clients[location]
            except KeyError:
                exeenv = self.get_execution_environments_info()[location] 
                self.logger.debug("Not found in cache ExecutionEnvironment {%s}! Starting it at %s:%d",
                                   location, exeenv.hostname, exeenv.port)
                execution_client = EEClient(exeenv.hostname, exeenv.port)
                self.ready_clients[location] = execution_client
    
            # Call EE
            self.logger.verbose("Calling make persistent to EE %s ", location)
            execution_client.make_persistent(settings.current_session_id, serialized_objs)

            # update the hint with the location, and return it
            instance.set_hint(location)
            
            # remove volatiles under deserialization
            self.remove_volatiles_under_deserialization()
            
        if alias is not None:
            # Add a new alias to an object.
            # Use cases:
            # 1 - object was persisted without alias and not yet registered -> we need to register it with new alias.
            # 2 - object was persisted and it is already registered -> we only add a new alias
            # 3 - object was persisted with an alias and it must be already registered -> we add a new alias.

            # From client side, we cannot check if object is registered or not (we do not have isPendingToRegister like EE)
            # Therefore, we call LogicModule with all information for registration.
            reg_info = [instance.get_object_id(), instance.get_class_extradata().class_id,
                        self.get_session_id(), instance.get_dataset_id()]
            self.ready_clients["@LM"].register_object(reg_info, location, alias, LANG_PYTHON)
        
            self.alias_cache[alias] = instance.get_object_id(), instance.get_class_extradata().class_id, location
        
        return location
    
    def add_session_reference(self, object_id):
        """
        @summary Add +1 reference associated to thread session
        @param object_id ID of object.
        """
        pass
    
    def execute_implementation_aux(self, operation_name, instance, parameters, exeenv_id=None):
        stub_info = instance.get_class_extradata().stub_info
        implementation_stub_infos = stub_info.implementations
        object_id = instance.get_object_id()
        
        self.logger.verbose("Calling operation '%s' in object with ID %s", operation_name, object_id)
        self.logger.debug("Call is being done into %r with #%d parameters",
                          instance, len(parameters))
        
        if instance.get_hint() is not None:
            exeenv_id = instance.get_hint()
            self.logger.verbose("Using hint = %s", exeenv_id)
        else:
            exeenv_id = self.get_execution_environment_by_oid(object_id)
    
        # // === SERIALIZE PARAMETERS === //
        serialized_params = serialize_params_or_return(
            params=parameters,
            iface_bitmaps=None,
            params_spec=implementation_stub_infos[operation_name].parameters,
            params_order=implementation_stub_infos[operation_name].paramsOrder,
            hint_volatiles=exeenv_id,
            runtime=self)
        
        remote_impl = [implementation_stub_infos[operation_name].remoteImplID,
                       implementation_stub_infos[operation_name].contractID,
                       implementation_stub_infos[operation_name].interfaceID]
    
        # // === EXECUTE === //
        max_retry = 3
        last_exception = None
        for k in range(max_retry):
            try:
                self.logger.verbose("Obtaining API for remote execution in %s ", exeenv_id)
                execution_client = self.ready_clients[exeenv_id]
            except KeyError:
                exeenv = self.get_execution_environments_info()[exeenv_id] 
                self.logger.debug("Not found in cache ExecutionEnvironment {%s}! Starting it at %s:%d",
                               exeenv_id, exeenv.hostname, exeenv.port)
                execution_client = EEClient(exeenv.hostname, exeenv.port)
                self.ready_clients[exeenv_id] = execution_client
    
            try:
                self.logger.verbose("Calling remote EE %s ", exeenv_id)
                ret = execution_client.ds_execute_implementation(
                    object_id,
                    remote_impl[0],
                    settings.current_session_id,
                    serialized_params)
                break
            
            except (DataClayException, RpcError) as dce:
                last_exception = dce
                self.logger.debug("Exception dataclay during execution. Retrying...")
                self.logger.debug(str(dce))
                metadata = self.ready_clients["@LM"].get_metadata_by_oid(
                    settings.current_session_id, object_id)
                new_location = False

                if metadata is None:
                    self.logger.warning("Execution failed and no metadata available. Cannot continue")
                    raise

                for loc in metadata.locations:
                    self.logger.debug("Found location %s" % str(loc))
                    if loc != exeenv_id:
                        exeenv_id = loc
                        self.logger.debug("Found different location %s" % str(loc))
                        new_location = True
                        break
                    
                if not new_location: 
                    exeenv_id = next(iter(metadata.locations))
                
                self.logger.debug("Retry in location %s" % str(exeenv_id))
     
                if self.logger.isEnabledFor(logging.DEBUG):
                    self.logger.debug("MetaDataInfo received for object: %s", object_id)
        else:
            raise last_exception
    
        self.logger.verbose("Result of operation named '%s' received", operation_name)
    
        if ret is None:
            return None
        else:
            return deserialize_return(
                ret, None, implementation_stub_infos[operation_name].returnType, self)

    def run_remote(self, object_id, backend_id, operation_name, value):
        try:
            execution_client = self.ready_clients[backend_id]
        except KeyError:
            exeenv = self.get_execution_environments_info()[backend_id]
            execution_client = EEClient(exeenv.hostname, exeenv.port)
            self.ready_clients[backend_id] = execution_client
            
        dcc_extradata = self.get_object_by_id(object_id).get_class_extradata()
        stub_info = dcc_extradata.stub_info
        implementation_stub_infos = stub_info.implementations
        operation = implementation_stub_infos[operation_name]
        value = serialize_params_or_return(
            params=(value,),
            iface_bitmaps=None,
            params_spec=operation.parameters,
            params_order=operation.paramsOrder,
            hint_volatiles=None,
            runtime=self
        )

        ret = execution_client.ds_execute_implementation(object_id, operation.remoteImplID, settings.current_session_id, value)

        if ret is not None:
            return deserialize_return(ret, None, operation.returnType, self)

    def call_execute_to_external_DC(self, instance, params, operation_name, dc_info):
        
        volatile_parameters_being_send = set()
        executed = False
        num_misses = 0
        stub_info = instance.get_class_extradata().stub_info
        implementation_stub_infos = stub_info.implementations
        operation = implementation_stub_infos[operation_name]
        dataclay_id = dc_info.dcID
        # === SERIALIZE PARAMETERS === 
        # Between DC - DC , ifaceBitMaps = null
        serialized_params = serialize_params_or_return(
            params=params,
            iface_bitmaps=None,
            params_spec=implementation_stub_infos[operation_name].parameters,
            params_order=implementation_stub_infos[operation_name].paramsOrder,
            hint_volatiles=instance.get_hint(),
            runtime=self)

        if serialized_params is not None and serialized_params[3] is not None:
            for param in serialized_params[3]:
                volatile_parameters_being_send.add(param[0])
        
        # TODO: Populate impl_info
        impl_info = list()

        while not executed and num_misses < 5:  # TODO: num_misses < Configuration.flags....
            try:
                self.logger.debug("[==JUMP==] Request execution to external dataClay named %s for object %s"
                , dc_info.name, instance.get_object_id())
                lm_client = self.ready_clients[dataclay_id]   
                
            except KeyError:
                lm_client = LMClient(dc_info.host, dc_info.port)
                
                self.ready_clients[dataclay_id] = lm_client

            try:
                ser_result = lm_client.execute_on_federated_object(dataclay_id, instance.get_object_id(), impl_info, serialized_params)
                executed = True
            except Exception:
                is_race_condition = False
                if serialized_params is not None and serialized_params[4] is not None:
                    for param in serialized_params[4]:
                        if param[0] in volatile_parameters_being_send:
                            is_race_condition = True
                            time.sleep(3)
                        break
            if not is_race_condition:
                num_misses += 1
        
        if num_misses > 0 and serialized_params is not None:
            for volatil in serialized_params[3]:
                volatile_parameters_being_send.remove(volatil[0])
        if not executed:
            self.logger.error("Trying to execute remotely object %s of class %s but something went wrong. Maybe the object is still not stored  (in case of asynchronous makepersistent) and waiting time is not enough. Maybe the object does not exist anymore due to a remove. Or Maybe an exception happened in the server and the call failed.",
            instance.get_object_id(),
            instance.get_class_extradata().name)

            raise RuntimeError("[dataClay] ERROR: Trying to execute remotely object  but something went wrong. Maybe the object is still not stored (in case of asynchronous makepersistent) and waiting time is not enough. Maybe the object does not exist anymore due to a remove. Or Maybe an exception happened in the server and the call failed.")
        
        return deserialize_return(serialized_params, None, operation.returnType, self)
    
    def close_session(self):
         self.ready_clients["@LM"].close_session(settings.current_session_id)

    def get_hint(self):
        return None
    
    def get_session_id(self):
        return settings.current_session_id
