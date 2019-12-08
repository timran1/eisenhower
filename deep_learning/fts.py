from ft_template import *


####
class CPU(DeepLearning_FT_Template):

    def __init__(self):
        super().__init__()
        self.name = "Unicore RISCV"

        try:

            # Extend utilizability to include any special HW features
            # CPU has multiple types of datapaths
            datapaths_set = self.find_sub_f("system.nodetypes_set.node.datapaths_set")[0]
            datapath_template = self.find_sub_f("system.nodetypes_set.node.datapaths_set.datapath")[0]
            datapaths_set.sub_features.remove(datapath_template)
            datapaths_set.sub_features.append(CPU.get_scalar_datapath(datapath_template))

            # Assign values to remaining features
            ##

            [f.init(num_dims=1) for f in self.find_sub_f("system.memory.num_cache")]
            [f.init(num_dims=2) for f in self.find_sub_f("system.memory.num_access_gran")] # Cache block size, reg size
            [f.init(num_dims=2) for f in self.find_sub_f("system.nodetypes_set.node.control.data_dep")] # SW based

        except KeyError as e:
            logging.exception(e)
            exit(-1)


    @staticmethod
    def get_scalar_datapath(template):

        scalar_datapath = copy.deepcopy(template)
        scalar_datapath.init(name="scalar", description="Scalar Datapath")

        [f.init(num_dims=0) for f in scalar_datapath.find_sub_f("scalar.num_dims_operation")]
        [f.init(num_dims=0) for f in scalar_datapath.find_sub_f("scalar.num_dims_mask")]
        [f.init(num_dims=1) for f in scalar_datapath.find_sub_f("scalar.num_mem_levels")]   # Normal registers
        [f.init(num_dims=0) for f in scalar_datapath.find_sub_f("scalar.latency_hide")]

        return scalar_datapath

####
class Intel_Xeon_Skylake_CPU(CPU):

    def __init__(self):
        super().__init__()
        self.name = "Xeon Skylake"

        try:

            # Add vector datapath
            datapaths_set = self.find_sub_f("system.nodetypes_set.node.datapaths_set")[0]
            datapath_template = self.find_sub_f("system.nodetypes_set.node.datapaths_set.scalar")[0]
            datapaths_set.sub_features.append(Intel_Xeon_Skylake_CPU.get_avx_datapath(datapath_template))

            # Assign values to remaining features
            ##
            [f.init(num_dims=3) for f in self.find_sub_f("system.memory.num_cache")]
            [f.init(num_dims=1) for f in self.find_sub_f("system.nodetypes_set.node.control.latency_hide")] # thread

            # Network: NUMA nodes in single socket
            [f.init(num_dims=2) for f in self.find_sub_f("system.network.num_latency")]   # SNC, NUMA
            [f.init(num_dims=2) for f in self.find_sub_f("system.network.num_bandwidth")]   # SNC, NUMA
            [f.init(num_dims=1) for f in self.find_sub_f("system.network.num_topology")]  # Linear layout
            [f.init(num_dims=2) for f in self.find_sub_f("system.network.num_sync_capability")]   # atomic, interrupt

        except KeyError as e:
            logging.exception(e)
            exit(-1)

    @staticmethod
    def get_avx_datapath(template):

        vector_datapath = copy.deepcopy(template)
        vector_datapath.init(name="avx", description="AVX Datapath")

        [f.init(num_dims=1) for f in vector_datapath.find_sub_f("avx.num_dims_operation")]
        [f.init(num_dims=0) for f in vector_datapath.find_sub_f("avx.num_dims_mask")]
        [f.init(num_dims=1) for f in vector_datapath.find_sub_f("avx.num_mem_levels")]
        [f.init(num_dims=0) for f in vector_datapath.find_sub_f("avx.latency_hide")]    # threading contexts, sw managed double buffering

        return vector_datapath

####
class NVIDIA_Fermi_GPU(CPU):

    def __init__(self):
        super().__init__()
        self.name = "NVIDIA Fermi"

        try:

            # Extend utilizability to include any special HW features
            # Add vector datapath
            datapaths_set = self.find_sub_f("system.nodetypes_set.node.datapaths_set")[0]
            datapath_template = self.find_sub_f("system.nodetypes_set.node.datapaths_set.scalar")[0]
            datapaths_set.sub_features.remove(datapath_template)
            datapaths_set.sub_features.append(NVIDIA_Fermi_GPU.get_cuda_datapath(datapath_template))

            # Memory
            [f.init(num_dims=1) for f in self.find_sub_f("system.memory.num_cache")]  # L2 / global
            [f.init(num_dims=2) for f in self.find_sub_f("system.memory.num_scratch")]   # Reg file, L1 (cache/scratc)
            [f.init(num_dims=1) for f in self.find_sub_f("system.memory.num_props")]  # Cache vs scratch

            # Node
            [f.init(num_dims=1) for f in self.find_sub_f("system.nodetypes_set.node.data_mov.local_dma")]
            [f.init(num_dims=1) for f in self.find_sub_f("system.nodetypes_set.node.control.latency_hide")]   # Thread
            [f.init(num_dims=2) for f in self.find_sub_f("system.nodetypes_set.node.control.data_dep")] # SW based

            # Network: L1 is local to each SM. Making a NUMA-like situation
            [f.init(num_dims=2) for f in self.find_sub_f("system.network.num_latency")]
            [f.init(num_dims=2) for f in self.find_sub_f("system.network.num_bandwidth")]
            [f.init(num_dims=1) for f in self.find_sub_f("system.network.num_sync_capability")]

        except KeyError as e:
            logging.exception(e)
            exit(-1)


    @staticmethod
    def get_cuda_datapath(template):

        vector_datapath = copy.deepcopy(template)
        vector_datapath.init(name="cuda", description="CUDA Datapath")

        [f.init(num_dims=2) for f in vector_datapath.find_sub_f("cuda.num_dims_operation")]
        [f.init(num_dims=1) for f in vector_datapath.find_sub_f("cuda.num_dims_mask")]
        [f.init(num_dims=0) for f in vector_datapath.find_sub_f("cuda.num_mem_levels")]
        [f.init(num_dims=0) for f in vector_datapath.find_sub_f("cuda.latency_hide")]

        return vector_datapath


####
class NVIDIA_Turing_GPU(NVIDIA_Fermi_GPU):

    def __init__(self):
        super().__init__()
        self.name = "NVIDIA Turing"

        try:

            # Extend utilizability to include any special HW features
            # Add Tensor datapath
            datapaths_set = self.find_sub_f("system.nodetypes_set.node.datapaths_set")[0]
            cuda_datapath = datapaths_set.find_sub_f("datapaths_set.cuda")[0]
            datapaths_set.sub_features.append(NVIDIA_Turing_GPU.get_tensor_datapath(cuda_datapath))

            # Separate CUDA cores for INT and FP operations. However they are both very similar just 
            # data type is different. Hence not setting it as 2 different datapaths.

        except KeyError as e:
            logging.exception(e)
            exit(-1)

    @staticmethod
    def get_tensor_datapath(template):

        tensor_datapath = copy.deepcopy(template)
        tensor_datapath.init(name="tensor", description="Tensor Datapath")

        [f.init(num_dims=3) for f in tensor_datapath.find_sub_f("tensor.num_dims_operation")]   # array of 2D datapaths
        [f.init(num_dims=2) for f in tensor_datapath.find_sub_f("tensor.num_dims_mask")]    # No control in inner 2 dims
        [f.init(num_dims=0) for f in tensor_datapath.find_sub_f("tensor.num_mem_levels")]
        [f.init(num_dims=0) for f in tensor_datapath.find_sub_f("tensor.latency_hide")]

        return tensor_datapath


####
class VTA(CPU):

    def __init__(self):
        super().__init__()
        self.name = "TVM's VTA"

        try:

            # Extend utilizability to include any special HW features
            # Add ALU and GEMM datapaths
            # Remove Scalar datapath
            datapaths_set = self.find_sub_f("system.nodetypes_set.node.datapaths_set")[0]
            scalar_datapath = datapaths_set.find_sub_f("datapaths_set.scalar")[0]
            datapaths_set.sub_features.remove(scalar_datapath)
            datapaths_set.sub_features.append(VTA.get_ALU_datapath(scalar_datapath))
            datapaths_set.sub_features.append(VTA.get_GEMM_datapath(scalar_datapath))

            # Assign values to remaining features
            ##

            # Memory
            [f.init(num_dims=0) for f in self.find_sub_f("system.memory.num_cache")]
            [f.init(num_dims=1) for f in self.find_sub_f("system.memory.num_scratch")] # L1: Input, weight, output, reg file
            [f.init(num_dims=3) for f in self.find_sub_f("system.memory.num_props")]  # Input vs weight vs reg file vs output

            # Node
            [f.init(num_dims=1) for f in self.find_sub_f("system.nodetypes_set.node.data_mov.local_dma")] # DMA exists
            [f.init(num_dims=2) for f in self.find_sub_f("system.nodetypes_set.node.data_mov.num_stride")]    # 2D stride
            [f.init(num_dims=2) for f in self.find_sub_f("system.nodetypes_set.node.control.loop_levels")]    # 2 levels
            [f.init(num_dims=1) for f in self.find_sub_f("system.nodetypes_set.node.control.latency_hide")] # ?
            [f.init(num_dims=1) for f in self.find_sub_f("system.nodetypes_set.node.control.data_dep")]  # DAE style

        except KeyError as e:
            logging.exception(e)
            exit(-1)


    @staticmethod
    def get_ALU_datapath(template):

        datapath = copy.deepcopy(template)
        datapath.init(name="alu", description="ALU Datapath")

        [f.init(num_dims=1) for f in datapath.find_sub_f("alu.num_dims_operation")]
        [f.init(num_dims=1) for f in datapath.find_sub_f("alu.num_dims_mask")]
        [f.init(num_dims=0) for f in datapath.find_sub_f("alu.num_mem_levels")]
        [f.init(num_dims=0) for f in datapath.find_sub_f("alu.latency_hide")]

        return datapath

    @staticmethod
    def get_GEMM_datapath(template):

        datapath = copy.deepcopy(template)
        datapath.init(name="gemm", description="GEMM Datapath")

        [f.init(num_dims=2) for f in datapath.find_sub_f("gemm.num_dims_operation")]
        [f.init(num_dims=2) for f in datapath.find_sub_f("gemm.num_dims_mask")]
        [f.init(num_dims=0) for f in datapath.find_sub_f("gemm.num_mem_levels")]
        [f.init(num_dims=0) for f in datapath.find_sub_f("gemm.latency_hide")]

        return datapath





####
class Tesla_NNA(CPU):

    def __init__(self):
        super().__init__()
        self.name = "Tesla NNA"

        try:

            # Extend utilizability to include any special HW features
            datapaths_set = self.find_sub_f("system.nodetypes_set.node.datapaths_set")[0]
            scalar_datapath = datapaths_set.find_sub_f("datapaths_set.scalar")[0]
            datapaths_set.sub_features.remove(scalar_datapath)
            datapaths_set.sub_features.append(Tesla_NNA.get_main_datapath(scalar_datapath))

            # Assign values to remaining features
            ##

            # Memory
            [f.init(num_dims=0) for f in self.find_sub_f("system.memory.num_cache")]
            [f.init(num_dims=2) for f in self.find_sub_f("system.memory.num_scratch")] # L1: SRAM banks, L2: (Weight, Block Cache)
            [f.init(num_dims=1) for f in self.find_sub_f("system.memory.num_props")] # Weight vs Block Cache

            # Node
            [f.init(num_dims=1) for f in self.find_sub_f("system.nodetypes_set.node.data_mov.local_dma")] # DMA exists
            [f.init(num_dims=2) for f in self.find_sub_f("system.nodetypes_set.node.data_mov.num_stride")]    # 2D stride
            [f.init(num_dims=1) for f in self.find_sub_f("system.nodetypes_set.node.control.loop_levels")]    # Loop construct in ISA, at least 1 level
            [f.init(num_dims=0) for f in self.find_sub_f("system.nodetypes_set.node.control.latency_hide")] # ? Not sure
            [f.init(num_dims=1) for f in self.find_sub_f("system.nodetypes_set.node.control.data_dep")]  # Some OoO with DMA and compute

        except KeyError as e:
            logging.exception(e)
            exit(-1)


    @staticmethod
    def get_main_datapath(template):

        datapath = copy.deepcopy(template)
        datapath.init(name="main", description="Main Datapath")

        [f.init(num_dims=2) for f in datapath.find_sub_f("main.num_dims_operation")]
        [f.init(num_dims=2) for f in datapath.find_sub_f("main.num_dims_mask")]
        [f.init(num_dims=2) for f in datapath.find_sub_f("main.num_mem_levels")] # input, output
        [f.init(num_dims=0) for f in datapath.find_sub_f("main.latency_hide")]

        return datapath



####
class TPU(CPU):

    def __init__(self):
        super().__init__()
        self.name = "Google TPU"

        try:

            # Extend utilizability to include any special HW features
            # Add ALU and GEMM datapaths
            # Remove Scalar datapath
            datapaths_set = self.find_sub_f("system.nodetypes_set.node.datapaths_set")[0]
            scalar_datapath = datapaths_set.find_sub_f("datapaths_set.scalar")[0]
            datapaths_set.sub_features.remove(scalar_datapath)
            datapaths_set.sub_features.append(TPU.get_main_datapath(scalar_datapath))

            # Assign values to remaining features
            ##

            # Memory
            [f.init(num_dims=1) for f in self.find_sub_f("system.memory.num_cache")] # weight FIFO
            [f.init(num_dims=1) for f in self.find_sub_f("system.memory.num_scratch")]    # L1: Systolic Data
            [f.init(num_dims=0) for f in self.find_sub_f("system.memory.num_props")]  # UB vs Weight Fifo

            # Stride info not available

            # Node
            [f.init(num_dims=1) for f in self.find_sub_f("system.nodetypes_set.node.data_mov.local_dma")] # DMA present
            [f.init(num_dims=1) for f in self.find_sub_f("system.nodetypes_set.node.data_mov.num_stride")] # Suppose 2D stride
            [f.init(num_dims=0) for f in self.find_sub_f("system.nodetypes_set.node.control.latency_hide")]   # No info
            [f.init(num_dims=1) for f in self.find_sub_f("system.nodetypes_set.node.control.data_dep")]   # DAE based

        except KeyError as e:
            logging.exception(e)
            exit(-1)


    @staticmethod
    def get_main_datapath(template):

        datapath = copy.deepcopy(template)
        datapath.init(name="main", description="Main Datapath")

        [f.init(num_dims=2) for f in datapath.find_sub_f("main.num_dims_operation")]
        [f.init(num_dims=2) for f in datapath.find_sub_f("main.num_dims_mask")]
        [f.init(num_dims=1) for f in datapath.find_sub_f("main.num_mem_levels")]    # Systolic data setup
        [f.init(num_dims=1) for f in datapath.find_sub_f("main.latency_hide")]  # Double buffering @ accumulator

        return datapath




class Simba(CPU):

    def __init__(self):
        super().__init__()
        self.name = "Simba"

        try:

            # Extend utilizability to include any special HW features
            # Add ALU and GEMM datapaths
            # Remove Scalar datapath
            datapaths_set = self.find_sub_f("system.nodetypes_set.node.datapaths_set")[0]
            scalar_datapath = datapaths_set.find_sub_f("datapaths_set.scalar")[0]
            datapaths_set.sub_features.remove(scalar_datapath)
            datapaths_set.sub_features.append(Simba.get_simba_pe_datapath(scalar_datapath))
            datapaths_set.sub_features.append(Simba.get_global_pe_scalar_datapath(scalar_datapath))

            # Assign values to remaining features
            ##

            # Memory
            [f.init(num_dims=0) for f in self.find_sub_f("system.memory.num_cache")]
            [f.init(num_dims=2) for f in self.find_sub_f("system.memory.num_scratch")] # L1: Input, weight, output, L2 = Global PE
            [f.init(num_dims=0) for f in self.find_sub_f("system.memory.num_props")]

            # Node - Global PE
            [f.init(num_dims=1) for f in self.find_sub_f("system.nodetypes_set.node.data_mov.local_dma")] # DMA exists
            [f.init(num_dims=2) for f in self.find_sub_f("system.nodetypes_set.node.data_mov.num_stride")]    # 2D stride (assumed)
            [f.init(num_dims=2) for f in self.find_sub_f("system.nodetypes_set.node.data_mov.num_pattern")] # Unicast, Multicast
            [f.init(num_dims=0) for f in self.find_sub_f("system.nodetypes_set.node.control.loop_levels")]    # Can work on global PE directly
            [f.init(num_dims=0) for f in self.find_sub_f("system.nodetypes_set.node.control.indirect_addr")]  # Yes 
            [f.init(num_dims=0) for f in self.find_sub_f("system.nodetypes_set.node.control.latency_hide")] # ?
            [f.init(num_dims=2) for f in self.find_sub_f("system.nodetypes_set.node.control.data_dep")]  # SW only

            # Network
            [f.init(num_dims=1) for f in self.find_sub_f("system.network.num_latency")]  # package level
            [f.init(num_dims=1) for f in self.find_sub_f("system.network.num_bandwidth")]  # package level
            [f.init(num_dims=3) for f in self.find_sub_f("system.network.num_topology")]  # 3 possible positions
            [f.init(num_dims=1) for f in self.find_sub_f("system.network.num_sync_capability")]   # Atomic access

        except KeyError as e:
            logging.exception(e)
            exit(-1)

    @staticmethod
    def get_simba_pe_datapath(template):

        datapath = copy.deepcopy(template)
        datapath.init(name="simba_pe", description="Simba PE Datapath")

        [f.init(num_dims=3) for f in datapath.find_sub_f("simba_pe.num_dims_operation")]
        [f.init(num_dims=2) for f in datapath.find_sub_f("simba_pe.num_dims_mask")]
        [f.init(num_dims=1) for f in datapath.find_sub_f("simba_pe.num_mem_levels")]
        [f.init(num_dims=0) for f in datapath.find_sub_f("simba_pe.latency_hide")]

        return datapath

    @staticmethod
    def get_global_pe_scalar_datapath(template):

        datapath = copy.deepcopy(template)
        datapath.init(name="global_pe_scalar", description="Global PE Scalar Datapath")

        [f.init(num_dims=0) for f in datapath.find_sub_f("global_pe_scalar.num_dims_operation")]
        [f.init(num_dims=0) for f in datapath.find_sub_f("global_pe_scalar.num_dims_mask")]
        [f.init(num_dims=1) for f in datapath.find_sub_f("global_pe_scalar.num_mem_levels")]
        [f.init(num_dims=0) for f in datapath.find_sub_f("global_pe_scalar.latency_hide")]

        return datapath



###
class Intel_SpringHill(CPU):

    def __init__(self):
        super().__init__()
        self.name = "Intel SH"

        try:

            # Add 2 node types
            node_set = self.find_sub_f("system.nodetypes_set")[0]
            node = node_set.find_sub_f("nodetypes_set.node")[0]
            node_set.sub_features.remove(node)
            node_set.sub_features.append(Intel_SpringHill.get_DSP_node(node))   # ICE DSP node
            node_set.sub_features.append(Intel_SpringHill.get_DL_grid_node(node))   # ICE DL grid node
            node_set.sub_features.append(Intel_SpringHill.get_IA_SNC_node(node))   # The IA SNC node

            # Assign values to remaining features
            ##

            # Memory
            [f.init(num_dims=1) for f in self.find_sub_f("system.memory.num_cache")]  # LLC
            [f.init(num_dims=2) for f in self.find_sub_f("system.memory.num_scratch")] # ICE: (SRAM => TCM), SNC(L1, L2 Caches)
            [f.init(num_dims=0) for f in self.find_sub_f("system.memory.num_props")]  # No props

            # Network
            [f.init(num_dims=2) for f in self.find_sub_f("system.network.num_latency")]  # (inside ICE, SNC core), #2: ring
            [f.init(num_dims=2) for f in self.find_sub_f("system.network.num_bandwidth")]  # (inside ICE, SNC core), #2: ring
            [f.init(num_dims=1) for f in self.find_sub_f("system.network.num_topology")]  # 1 possible position - ring
            [f.init(num_dims=2) for f in self.find_sub_f("system.network.num_sync_capability")]   # Atomic access, (HW sync b/w DSP and grid, interrupts for SNC)

        except KeyError as e:
            logging.exception(e)
            exit(-1)


    @staticmethod
    def get_DSP_node(template):

        node = copy.deepcopy(template)
        node.init(name="dsp", description="DSP Node")

        datapaths_set = node.find_sub_f("dsp.datapaths_set")[0]
        scalar_datapath = datapaths_set.find_sub_f("datapaths_set.scalar")[0]
        datapaths_set.sub_features.remove(scalar_datapath)
        datapaths_set.sub_features.append(Intel_SpringHill.get_DSP_vector_datapath(scalar_datapath))
        datapaths_set.sub_features.append(Intel_SpringHill.get_DSP_scalar_datapath(scalar_datapath))

        # Node
        [f.init(num_dims=1) for f in node.find_sub_f("dsp.data_mov.local_dma")] # DMA exists
        [f.init(num_dims=1) for f in node.find_sub_f("dsp.data_mov.num_stride")]    # 2D DMA = 1D stride - from Tenscilica page
        [f.init(num_dims=3) for f in node.find_sub_f("dsp.data_mov.num_pattern")] # Unicast, Scatter, Gather
        [f.init(num_dims=0) for f in node.find_sub_f("dsp.control.loop_levels")]    # 0 
        [f.init(num_dims=0) for f in node.find_sub_f("dsp.control.indirect_addr")]  # Yes
        [f.init(num_dims=0) for f in node.find_sub_f("dsp.control.latency_hide")] # None in DSP ?
        [f.init(num_dims=2) for f in node.find_sub_f("dsp.control.data_dep")]  # SW only

        return node


    @staticmethod
    def get_DSP_vector_datapath(template):

        datapath = copy.deepcopy(template)
        datapath.init(name="dsp_vec", description="DSP Vector Datapath")

        [f.init(num_dims=1) for f in datapath.find_sub_f("dsp_vec.num_dims_operation")]
        [f.init(num_dims=0) for f in datapath.find_sub_f("dsp_vec.num_dims_mask")]
        [f.init(num_dims=1) for f in datapath.find_sub_f("dsp_vec.num_mem_levels")]
        [f.init(num_dims=0) for f in datapath.find_sub_f("dsp_vec.latency_hide")]

        return datapath


    @staticmethod
    def get_DSP_scalar_datapath(template):

        datapath = copy.deepcopy(template)
        datapath.init(name="dsp_sca", description="DSP Scalar Datapath")

        [f.init(num_dims=0) for f in datapath.find_sub_f("dsp_sca.num_dims_operation")]
        [f.init(num_dims=0) for f in datapath.find_sub_f("dsp_sca.num_dims_mask")]
        [f.init(num_dims=1) for f in datapath.find_sub_f("dsp_sca.num_mem_levels")]
        [f.init(num_dims=0) for f in datapath.find_sub_f("dsp_sca.latency_hide")]

        return datapath


    @staticmethod
    def get_DL_grid_node(template):
        node = copy.deepcopy(template)
        node.init(name="dl_grid", description="DL Grid Node")

        datapaths_set = node.find_sub_f("dl_grid.datapaths_set")[0]
        scalar_datapath = datapaths_set.find_sub_f("datapaths_set.scalar")[0]
        datapaths_set.sub_features.remove(scalar_datapath)
        datapaths_set.sub_features.append(Intel_SpringHill.get_DL_compute_datapath(scalar_datapath))

        # Node
        [f.init(num_dims=1) for f in node.find_sub_f("dl_grid.data_mov.local_dma")] # DMA exists
        [f.init(num_dims=5) for f in node.find_sub_f("dl_grid.data_mov.num_stride")]    # 3D stride (2D grid for 5D stride)
        [f.init(num_dims=2) for f in node.find_sub_f("dl_grid.data_mov.num_pattern")] # Unicast, Broadcast
        [f.init(num_dims=0) for f in node.find_sub_f("dl_grid.control.loop_levels")] 
        [f.init(num_dims=1) for f in node.find_sub_f("dl_grid.control.indirect_addr")]  # No support in PEs
        [f.init(num_dims=0) for f in node.find_sub_f("dl_grid.control.latency_hide")] # Nothing
        [f.init(num_dims=2) for f in node.find_sub_f("dl_grid.control.data_dep")]  # SW only - prod-cons between DSP and grid captured in network

        return node


    @staticmethod
    def get_DL_compute_datapath(template):

        datapath = copy.deepcopy(template)
        datapath.init(name="dl_comp", description="DL Compute Grid Datapath")

        [f.init(num_dims=3) for f in datapath.find_sub_f("dl_comp.num_dims_operation")] # array of 2D PEs
        [f.init(num_dims=2) for f in datapath.find_sub_f("dl_comp.num_dims_mask")]
        [f.init(num_dims=2) for f in datapath.find_sub_f("dl_comp.num_mem_levels")] # Output registers, Internal OSRAM
        [f.init(num_dims=0) for f in datapath.find_sub_f("dl_comp.latency_hide")]

        return datapath


    @staticmethod
    def get_IA_SNC_node(template):
        node = copy.deepcopy(template)
        node.init(name="ia_snc", description="IA SNC Node")

        datapaths_set = node.find_sub_f("ia_snc.datapaths_set")[0]
        scalar_datapath = datapaths_set.find_sub_f("datapaths_set.scalar")[0]
        datapaths_set.sub_features.remove(scalar_datapath)
        datapaths_set.sub_features.append(Intel_SpringHill.get_IA_SNC_avx_datapath(scalar_datapath))
        datapaths_set.sub_features.append(Intel_SpringHill.get_IA_SNC_scalar_datapath(scalar_datapath))

        # Node
        [f.init(num_dims=0) for f in node.find_sub_f("ia_snc.data_mov.local_dma")] # No DMAs
        [f.init(num_dims=0) for f in node.find_sub_f("ia_snc.data_mov.num_stride")]    # No stride
        [f.init(num_dims=0) for f in node.find_sub_f("ia_snc.data_mov.num_pattern")] # No DMAs
        [f.init(num_dims=0) for f in node.find_sub_f("ia_snc.control.loop_levels")]    # Full functional core
        [f.init(num_dims=0) for f in node.find_sub_f("ia_snc.control.indirect_addr")]  # Yes
        [f.init(num_dims=1) for f in node.find_sub_f("ia_snc.control.latency_hide")] # Multithreading
        [f.init(num_dims=2) for f in node.find_sub_f("ia_snc.control.data_dep")]  # SW only - prod-cons between DSP and grid captured in network

        return node


    @staticmethod
    def get_IA_SNC_avx_datapath(template):

        datapath = copy.deepcopy(template)
        datapath.init(name="avx", description="AVX Datapath")

        [f.init(num_dims=1) for f in datapath.find_sub_f("avx.num_dims_operation")]
        [f.init(num_dims=0) for f in datapath.find_sub_f("avx.num_dims_mask")]
        [f.init(num_dims=1) for f in datapath.find_sub_f("avx.num_mem_levels")] # Output registers, Internal OSRAM
        [f.init(num_dims=0) for f in datapath.find_sub_f("avx.latency_hide")]

        return datapath


    @staticmethod
    def get_IA_SNC_scalar_datapath(template):

        datapath = copy.deepcopy(template)
        datapath.init(name="scalar", description="Scalar Datapath")

        [f.init(num_dims=0) for f in datapath.find_sub_f("scalar.num_dims_operation")]
        [f.init(num_dims=0) for f in datapath.find_sub_f("scalar.num_dims_mask")]
        [f.init(num_dims=1) for f in datapath.find_sub_f("scalar.num_mem_levels")] # Output registers, Internal OSRAM
        [f.init(num_dims=0) for f in datapath.find_sub_f("scalar.latency_hide")]

        return datapath





class Ada_Accel(CPU):

    def __init__(self):
        super().__init__()
        self.name = "Ada"

        try:

            # Extend utilizability to include any special HW features
            # Add ALU and GEMM datapaths
            # Remove Scalar datapath
            datapaths_set = self.find_sub_f("system.nodetypes_set.node.datapaths_set")[0]
            scalar_datapath = datapaths_set.find_sub_f("datapaths_set.scalar")[0]
            datapaths_set.sub_features.remove(scalar_datapath)
            datapaths_set.sub_features.append(Ada_Accel.get_main_datapath(scalar_datapath))
            datapaths_set.sub_features.append(Ada_Accel.get_control_datapath(scalar_datapath))

            # Assign values to remaining features
            ##

            # Memory
            [f.init(num_dims=1) for f in self.find_sub_f("system.memory.num_cache")]  # LLC
            [f.init(num_dims=1) for f in self.find_sub_f("system.memory.num_scratch")] # In PE
            [f.init(num_dims=0) for f in self.find_sub_f("system.memory.num_props")]  # 

            # Node
            [f.init(num_dims=1) for f in self.find_sub_f("system.nodetypes_set.node.data_mov.local_dma")] # DMA exists
            [f.init(num_dims=1) for f in self.find_sub_f("system.nodetypes_set.node.data_mov.num_stride")]    # 1D stride 
            [f.init(num_dims=2) for f in self.find_sub_f("system.nodetypes_set.node.data_mov.num_pattern")] # Unicast, Multicast
            [f.init(num_dims=0) for f in self.find_sub_f("system.nodetypes_set.node.control.loop_levels")]    # Full gen purpose each
            [f.init(num_dims=0) for f in self.find_sub_f("system.nodetypes_set.node.control.indirect_addr")]  # Yes
            [f.init(num_dims=0) for f in self.find_sub_f("system.nodetypes_set.node.control.latency_hide")] # None
            [f.init(num_dims=0) for f in self.find_sub_f("system.nodetypes_set.node.control.data_dep")]  # Scoreboard handled

            # Network
            [f.init(num_dims=1) for f in self.find_sub_f("system.network.num_latency")]  # NOC
            [f.init(num_dims=1) for f in self.find_sub_f("system.network.num_bandwidth")]  # NOC
            [f.init(num_dims=3) for f in self.find_sub_f("system.network.num_topology")]  # 2D grid
            [f.init(num_dims=1) for f in self.find_sub_f("system.network.num_sync_capability")]   # Atomic access

        except KeyError as e:
            logging.exception(e)
            exit(-1)


    @staticmethod
    def get_control_datapath(template):

        datapath = copy.deepcopy(template)
        datapath.init(name="control", description="Control Datapath")

        [f.init(num_dims=0) for f in datapath.find_sub_f("control.num_dims_operation")]
        [f.init(num_dims=0) for f in datapath.find_sub_f("control.num_dims_mask")]
        [f.init(num_dims=1) for f in datapath.find_sub_f("control.num_mem_levels")]    # Internal registers
        [f.init(num_dims=0) for f in datapath.find_sub_f("control.latency_hide")]

        return datapath

    @staticmethod
    def get_main_datapath(template):

        datapath = copy.deepcopy(template)
        datapath.init(name="main", description="Main Datapath")

        [f.init(num_dims=3) for f in datapath.find_sub_f("main.num_dims_operation")]
        [f.init(num_dims=2) for f in datapath.find_sub_f("main.num_dims_mask")]
        [f.init(num_dims=1) for f in datapath.find_sub_f("main.num_mem_levels")]    # Direct access to memory
        [f.init(num_dims=0) for f in datapath.find_sub_f("main.latency_hide")]

        return datapath
