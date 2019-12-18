# Deep Learning Feature Trees

This page outlines Backend Development Cost (BDC) analysis of Deep Learning accelerators. The Feature Tree Template (\<FT>) used for this analysis is available [below](#feature-tree-template). We used the provided \<FT> to model the following hardware:
* Unicore RISC-V CPU
* Intel Xeon CPU
* NVIDIA Fermi GPU
* NVIDIA Turing GPU
* Google TPU v1
* Versatile Tensor Accelerator (VTA)
* Intel Spring Hill
* NVIDIA Simba

## Feature Tree Template (\<FT>)



- **[System Root](#)** </br>  *combine =* SUM;  *weight =* 1 
  - **[Memory Hierarchy](#memory-hierarchy)** </br>  *combine =* SUM;  *weight =* 1 
    - **[Implicit Data Movement](#memory-hierarchy--implicit-data-movement)**: No. of cache levels </br> *stage_mask =* [0, 0, 1, 1];   *scale =* Linear; *weight =* 1 
    - **[Explicit Data Movement](#memory-hierarchy--explicit-data-movement)**: No. of scratchpad levels </br> *stage_mask =* [1, 1, 1, 1];   *scale =* Linear; *weight =* 1 
    - **[Software Coherency](#memory-hierarchy--software-coherency)**: No. of software coherrent levels </br> *stage_mask =* [0, 1, 0, 1];   *scale =* Linear; *weight =* 1 
    - **[Data Access Granularity](#memory-hierarchy--data-access-granularity)**: No. of data access granularity levels </br> *stage_mask =* [1, 1, 1, 1];   *scale =* Linear; *weight =* 1 
    - **[Storage Properties](#memory-hierarchy--storage-properties)**: No. of storage properties [Activations, Weights, Output] </br> *stage_mask =* [1, 0, 1, 0];   *scale =* Linear; *weight =* 1 
  - **[Node Types Set](#node-types-set)** </br>  *combine =* SUM;  *weight =* 1 
    - **[Node](#node-types-set--node)** </br>  *combine =* SUM;  *weight =* 1 
      - **[Data Movement](#node-types-set--node--data-movement)** </br>  *combine =* SUM;  *weight =* 1 
        - **[DMA Engines](#node-types-set--node--data-movement--dma-engines)**: DMA engines present in node [y/n] </br> *stage_mask =* [0, 0, 1, 1];   *scale =* Linear; *weight =* 1 
        - **[Stride](#node-types-set--node--data-movement--stride)**: No. of dimensions of hardware supported stride </br> *stage_mask =* [1, 0, 1, 0];   *scale =* Linear; *weight =* 1 
        - **[Patterns](#node-types-set--node--data-movement--patterns)**: No. of movement patterns [Peer-to-Peer, Broadcast, Scatter] </br> *stage_mask =* [0, 1, 0, 1];   *scale =* Linear; *weight =* 1 
      - **[Control](#node-types-set--node--control)** </br>  *combine =* SUM;  *weight =* 1 
        - **[Indirect Addressing](#node-types-set--node--control--indirect-addressing)**: Node supports indirect addressing [y/n] </br> *stage_mask =* [0, 1, 0, 0];   *scale =* Linear; *weight =* 1 
        - **[Loop Levels](#node-types-set--node--control--loop-levels)**: No. of loop levels from full control flow </br> *stage_mask =* [0, 1, 0, 0];   *scale =* Linear; *weight =* 1 
        - **[Latency Hiding](#node-types-set--node--control--latency-hiding)**: No. of latency hiding widgets [Threads, Double Buffers] </br> *stage_mask =* [0, 0, 1, 1];   *scale =* Exponential; *weight =* 1 
        - **[Data Dependency](#node-types-set--node--control--data-dependency)**: Sync. support between data producer and consumer </br> *stage_mask =* [1, 0, 1, 0];   *scale =* Linear; *weight =* 1 
        - **[ISA Specialization](#node-types-set--node--control--isa-specialization)**: Avg no. of ISA commands per operator </br> *stage_mask =* [1, 1, 1, 1];   *scale =* Linear; *weight =* 1 
      - **[Datapaths Set](#node-types-set--node--datapaths-set)** </br>  *combine =* SUM;  *weight =* 1 
        - **[DataPath](#node-types-set--node--datapaths-set--datapath)** </br>  *combine =* SUM;  *weight =* 1 
          - **[Operation Dimensions](#node-types-set--node--datapaths-set--datapath--operation-dimensions)**: No. of dimensions of data operations </br> *stage_mask =* [1, 0, 0, 0];   *scale =* Linear; *weight =* 1 
          - **[Unmaskable Dimensions](#node-types-set--node--datapaths-set--datapath--unmaskable-dimensions)**: No. of inner operation dimensions without masking support </br> *stage_mask =* [1, 0, 0, 0];   *scale =* Linear; *weight =* 1 
          - **[Memory Levels](#node-types-set--node--datapaths-set--datapath--memory-levels)**: No. of memory units in datapath [Input, Output, Internal] </br> *stage_mask =* [1, 0, 1, 0];   *scale =* Linear; *weight =* 1 
          - **[Latency Hiding](#node-types-set--node--datapaths-set--datapath--latency-hiding)**: No. of latency hiding widgets [Threads, Double Buffers] </br> *stage_mask =* [0, 0, 1, 0];   *scale =* Linear; *weight =* 1 
  - **[Network and Synchronization](#network-and-synchronization)** </br>  *combine =* SUM;  *weight =* 1 
    - **[Latency](#network-and-synchronization--latency)**: No. of latency domains visible to node </br> *stage_mask =* [0, 0, 0, 1];   *scale =* Linear; *weight =* 1 
    - **[Bandwidth](#network-and-synchronization--bandwidth)**: No. of bandwidth domains visible to node </br> *stage_mask =* [0, 0, 0, 1];   *scale =* Linear; *weight =* 1 
    - **[Topology Positions](#network-and-synchronization--topology-positions)**: No. of topology positions in node layout </br> *stage_mask =* [0, 0, 0, 1];   *scale =* Linear; *weight =* 1 
    - **[Sync Capability](#network-and-synchronization--sync-capability)**: No. of inter-node sync. capabilities [Atomics, Interrupt] </br> *stage_mask =* [0, 1, 0, 1];   *scale =* Linear; *weight =* 1 


## Backend Development Stages
TODO: Put diagram. discuss

## \<FT> Details
We now provide more details for the hardware features discussed in \<FT> above.

### Organization
The <FT> organizes Hardware Features Descriptors (HDFs) into following categories:
* Memory
* Node
    * Datapaths
    * Control
    * Data Movement
* Network and Synchronization

We differentiate between nodes and datapaths as follows. TODO: describe.

### Memory Hierarchy : Implicit Data Movement
This feature captures the number of cache levels in the memory hierarchy. Presence of cache is transparent to developers at functional stages. However, it is imperative for performance to employ loop tilling/blocking such that inner-most loop levels access data residing in closest cache levels.

### Memory Hierarchy : Explicit Data Movement
This feature captures the number of scratch levels in the memory hierarchy. Presence of scratchpads require developer attention even for the first functional version of backend. Hence, cache incurs BDC at all stages. 

### Memory Hierarchy : Software Coherency
Some levels of the memory hierarchy may delegate coherency management to the developer. The developer must ensure that multiple nodes accessing the same memory location can view the latest value. As cohrency is only relevant for multi-node scenarios, this feature incurs BDC at distributed backend development stages only.

### Network and Synchronization : Latency
TODO: Per feature details here

## References
TODO: Add
