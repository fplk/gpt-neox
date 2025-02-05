import subprocess
from dataclasses import dataclass
from .template import NeoXArgsTemplate
from typing import Literal

def get_git_commit_hash():
    """ Gets the git commit hash of your current repo (if it exists) """
    try:
        git_hash = subprocess.check_output(["git", "describe", "--always"]).strip()
        git_hash = git_hash.decode()
    except subprocess.CalledProcessError:
        git_hash = None
    return git_hash

@dataclass
class NeoXArgsParallelism(NeoXArgsTemplate):
    
    pipe_parallel_size: int = 0
    """
    Number of pipeline parallel stages. Disable with 0.
    """
    
    model_parallel_size: int = 1
    """
    Size of the model parallelism.
    """

    pipe_partition_method: str = "type:transformer"
    """
    method used to distribute model layers across pipeline stages. Choose from "parameters", which balances the number of parameters on each pipeline stage, "uniform", which naively balances the number of layers per stage, or "type:[regex]" (in our case this will basically only be "type:transformer"), which balances layers whose class names match [regex]
    """

    world_size: int = None
    """
    Total world size (i.e number of gpus in cluster). Configured post-launch using distributed launcher
    """


@dataclass
class NeoXArgsModel(NeoXArgsTemplate):

    precision: Literal["fp16", "fp32"] = None 
    """
    description of the used precision, either one of fp16 or fp32 (and in the future bf16).
    """

    num_layers: int = None
    """
    Number of transformer layers.
    """

    hidden_size: int = None
    """
    Transformer hidden size.
    """

    num_attention_heads: int = None
    """
    Number of transformer attention heads.
    """

    seq_length: int = None
    """
    Maximum sequence length to process.
    """

    max_position_embeddings: int = None
    """
    Maximum number of position embeddings to use. This is the size of position embedding.
    """

    norm: Literal['layernorm', 'rmsnorm', 'scalenorm'] = "layernorm"
    """
    Normalization layer to use. Choose from "layernorm", "rmsnorm" and "scalenorm".
    """

    layernorm_epsilon: float = 1.0e-5
    """
    Layer norm epsilon.
    """

    rms_norm_epsilon: float = 1.0e-8
    """
    Root mean squared norm epsilon
    """

    scalenorm_epsilon: float = 1.0e-8
    """
    Scalenorm epsilon
    """

    pos_emb: Literal['learned', 'rotary', 'sinusoidal', 'rpe', 'none'] = "learned"
    """
    Type of positional embedding to use - choose from 'learned', 'rotary', 'sinusoidal', 'rpe', 'none'
    """

    rpe_num_buckets: int = 32
    """
    T5 relative positional encoding number of buckets, default 32.
    """

    rpe_max_distance: int = 128
    """
    T5 relative positional encoding max distance, default 128.
    """

    no_weight_tying: bool = False
    """
    Disables weight tying between embedding weights and final Linear layer
    """

    geglu: bool = False
    """
    Enable geglu activation function (WARNING: will increase memory usage, adjust embd dims accordingly)
    """

    sparsity: Literal['all', 'interspersed', 'none'] = "none"
    """
    Sparse attention layer configuration: none = all regular attn, all = all sparse attn, interspersed = sparse on odd layers, dense on even.
    """

    num_unique_layers: int = None
    """
    Number of unique transformer layers. num-layers should be divisible by this value. Currently only has an effect when pipe_parallel_size=0.
    """

    param_sharing_style: str = "grouped"
    """
    Ordering of the shared parameters. For example, for a num-layers=4 and --num-unique-layers=2, we will have the following ordering for two unique layers 1 and 2-: grouped: [1, 2, 1, 2] and spaced: [1, 1, 2, 2].
    """

    make_vocab_size_divisible_by: int = 128
    """
    Pad the vocab size to be divisible by this value. This is added for computational efficiency reasons.
    """

    apply_residual_connection_post_layernorm: bool = False
    """
    If set, use original BERT residual connection ordering.
    """

    openai_gelu: bool = False
    """
    Use OpenAIs GeLU implementation. This option should not be used unless for backward compatibility reasons.
    """

    scaled_upper_triang_masked_softmax_fusion: bool = False
    """
    Enable fusion of query_key_value_scaling time (upper diagonal) masking and softmax.
    """

    scaled_masked_softmax_fusion: bool = False
    """
    Enable fusion of query_key_value_scaling general masking and softmax.
    """

    bias_gelu_fusion: bool = False
    """
    Enable bias and gelu fusion.
    """

    bias_dropout_fusion: bool = False
    """
    Enable bias and dropout fusion.
    """

    fp16_lm_cross_entropy: bool = False
    """
    Move the cross entropy unreduced loss calculation for lm head to fp16.
    """

    init_method_std: float = 0.02
    """
    Standard deviation of the zero mean normal distribution used for weight initialization.
    """

    apply_query_key_layer_scaling: bool = False
    """
    Scale Q * K^T by 1 / layer-number. If this flag is set, then it will automatically set attention-softmax-in-fp32 to true
    """

    use_cpu_initialization: bool = False
    """
    If set, affine parallel weights initialization uses CPU
    """

    attention_softmax_in_fp32: bool = False
    """
    Run attention masking and softmax in fp32.
    """
    
    rotary_pct: float = 1.0 
    """
    pct of hidden dims to apply rotary positional embedding to
    """

    rotary_emb_base: int = 10000 
    """
    Base for rotary positional embedding
    """


@dataclass
class NeoXArgsOptimizer(NeoXArgsTemplate):

    optimizer_type: Literal['adam', 'onebitadam', 'cpu_adam', 'cpu_torch_adam', 'sm3'] = "adam"
    """
    Type of optimizer to use. Choose from ['adam', 'onebitadam', 'cpu_adam', 'cpu_torch_adam', 'sm3']
    """

    zero_stage: int = None
    """
    Zero Optimizer stage
    """
    
    zero_reduce_scatter: bool = None
    """
    Zero: Uses reduce or reduce scatter instead of allreduce to average gradients
    """
    
    zero_contiguous_gradients: bool = None
    """
    Zero: Copies the gradients to a contiguous buffer as they are produced. Avoids memory fragmentation during backward pass. Only useful when running very large models.
    """
    
    zero_reduce_bucket_size: int = None
    """
    Zero: Number of elements reduced/allreduced at a time. Limits the memory required for the allgather for large model sizes
    """
    
    zero_allgather_bucket_size: int = None
    """
    Zero: Number of elements allgathered at a time. Limits the memory required for the allgather for large model sizes
    """

    lr: float = None 
    """
    Max Learning rate during training
    """


@dataclass
class NeoXArgsLRScheduler(NeoXArgsTemplate):
    lr_decay_style: Literal['constant', 'linear', 'cosine', 'exponential'] = "linear"
    """
    Learning rate decay function. Choose from 'constant', 'linear', 'cosine', 'exponential'.
    """

    lr_decay_iters: int = None
    """
    Number of iterations to decay learning rate over, If None defaults to --train-iters
    """

    min_lr: float = 0.0
    """
    Minumum value for learning rate. The scheduler clips values below this threshold.
    """

    warmup: float = 0.01
    """
    Percentage of total iterations to warmup on (.01 = 1 percent of all training iters).
    """

    override_lr_scheduler: bool = False
    """
    Reset the values of the scheduler (learning rate,warmup iterations, minimum learning rate, maximum number of iterations, and decay style from input arguments and ignore values from checkpoints. Note that all the above values will be reset.
    """

    use_checkpoint_lr_scheduler: bool = False
    """
    Use checkpoint to set the values of the scheduler (learning rate, warmup iterations, minimum learning rate, maximum number of iterations, and decay style from checkpoint and ignore input arguments.
    """


@dataclass
class NeoXArgsLogging(NeoXArgsTemplate):

    wandb_group: str = None
    """Weights and Biases group name - used to group together "runs"."""

    wandb_team: str = None
    """Team name for Weights and Biases."""

    git_hash: str = get_git_commit_hash()
    """current git hash of repository"""

    log_dir: str = None
    """
    Directory to save logs to.
    """

    tensorboard_dir: str = None
    """
    Write TensorBoard logs to this directory.
    """

    log_interval: int = None
    """
    Interval between logging.
    """

    log_param_norm: bool = False
    """
    Log the frob norm of the parameters to wandb / tensorboard (useful for debugging).
    """

    log_grad_norm: bool = False
    """
    Log the frob norm of the gradients to wandb / tensorboard (useful for debugging).
    (N.B - this will only work with pp = 0 for now, as we don't have access to the gradients of the model because 
    deepspeed.)
    """

    log_optimizer_states: bool = False
    """
    Log the frob norm of the optimizer states to wandb / tensorboard (useful for debugging).
    """

    log_gradient_noise_scale: bool = False
    """
    Whether to log the gradient noise scale when training (cf. https://arxiv.org/abs/1812.06162 for explanation) 
    """

    gradient_noise_scale_n_batches: int = 5
    """
    Number of batches to accumulate gradients for in the gradient noise scale logger.
    """

    gradient_noise_scale_cpu_offload: bool = False
    """
    Whether to offload the buffered gradients to cpu when measuring gradient noise scale.
    """


@dataclass
class NeoXArgsOther(NeoXArgsTemplate):

    distributed_backend: str = "nccl"
    """
    Which backend to use for distributed training.
    """

    local_rank: int = None
    """
    local rank passed from distributed launcher.
    """

    rank: int = None
    """
    global rank of process being run (passed in via distributed launcher)
    """

    lazy_mpu_init: bool = False
    """
    If set to True, initialize_megatron() skips DDP initialization and returns function to complete it instead. Also turns on use-cpu-initialization flag. This is for external DDP manager.
    """

    short_seq_prob: float = 0.1
    """
    Probability of producing a short sequence.
    """

    reset_position_ids: bool = False
    """
    Reset posistion ids after end-of-document token.
    """

    reset_attention_mask: bool = False
    """
    Reset self attention mask after end-of-document token.
    """

    eod_mask_loss: bool = False
    """
    Mask loss for the end of document tokens.
    """

    adlr_autoresume: bool = False
    """
    Enable auto-resume on adlr cluster.
    """

    adlr_autoresume_interval: int = 1000
    """
    Intervals over which check for auto-resume termination signal
    """

    seed: int = 1234
    """
    Random seed used for python, numpy, pytorch, and cuda.
    """

    onnx_safe: bool = False
    """
    Use workarounds for known problems with Torch ONNX exporter
    """

    deepscale: bool = False
    """
    (Deprecated) enable DeepSpeed (helper flag for user code, no impact on DeepSpeed backend)'
    """

    deepscale_config: str = None
    """(Deprecated) deepscale json configuration file."""

    deepspeed_mpi: bool = False
    """
    Run via MPI, this will attempt to discover the necessary variables to initialize torch distributed from the MPI environment
    """
    
    user_script: str = None
    """
    user script to be run
    """

    iteration: int = None
    """
    Set during training
    """

    do_train: int = None
    """
    Set during training
    """

    do_valid: int = None
    """
    Set during training
    """

    do_test: int = None
    """
    Set during training
    """

@dataclass
class NeoXArgsTokenizer(NeoXArgsTemplate):

    tokenizer_type: Literal["GPT2BPETokenizer", "HFTokenizer", "HFGPT2Tokenizer", "CharLevelTokenizer"] = "GPT2BPETokenizer"
    """
    Type of tokenizer to use - should be one of ["GPT2BPETokenizer", "HFTokenizer", "HFGPT2Tokenizer", "CharLevelTokenizer"]
    """

    padded_vocab_size: int = None
    """
    Total (padded) vocabulary size of tokenizer. Configured after launching of training, 
    as it's dependent on the parallelism size.
    """


@dataclass
class NeoXArgsTextgen(NeoXArgsTemplate):

    text_gen_type: str = None
    """
    How to generate text/sample the model.
    Options: `unconditional`, `input-file`, `interactive`
    """

    temperature: float = 1.0
    """
    Sampling temperature.
    """

    greedy: bool = False
    """
    Use greedy sampling.
    """

    top_p: float = 0.0
    """
    Top p sampling.
    """

    top_k: int = 0
    """
    Top k sampling.
    """

    out_seq_length: int = 1024
    """
    Size of the output generated text.'
    """

    sample_input_file: str = None
    """
    Get input from file instead of interactive mode, each line is an input.
    """

    sample_output_file: str = None
    """
    Output file got from --sample-input-file
    """

    num_samples: int = 0
    """
    Number of samples to generate unconditionally, defaults to 0 and interactive conditional sampling
    """

    genfile: str = None
    """
    Output file when generating unconditionally
    """

    recompute: bool = False
    """
    During generation recompute all attention instead of using previously computed keys/values.
    """


@dataclass
class NeoXArgsTraining(NeoXArgsTemplate):

    data_path: str = None
    """
    Path to combined dataset to split.
    """

    data_impl: str = 'infer'
    """
    Implementation of indexed datasets.
    """

    mmap_warmup: bool = False
    """
    Warm up mmap files.
    """

    save: str = None
    """
    Output directory to save checkpoints to.
    """

    load: str = None
    """
    Directory containing a model checkpoint.
    """

    save_interval: int = None
    """
    Number of iterations between checkpoint saves.
    """

    no_save_optim: bool = False
    """
    Do not save current optimizer.
    """

    no_save_rng: bool = False
    """
    Do not save current rng state.
    """

    no_load_optim: bool = False
    """
    Do not load optimizer when loading checkpoint.
    """

    no_load_rng: bool = False
    """
    Do not load rng state when loading checkpoint.
    """

    finetune: bool = False
    """
    Load model for finetuning. Do not load optimizer or rng state from checkpoint and set iteration to 0. Assumed when loading a release checkpoint.
    """

    batch_size: int = None
    """
    training microbatch size per gpu
    """

    train_iters: int = None
    """
    Number of iterations to run for training.
    """

    eval_iters: int = 100
    """
    Number of iterations to run for evaluation validation/test for.
    """

    keep_last_n_checkpoints: int = None
    """
    Number of last checkpoints to keep
    """

    eval_interval: int = 1000
    """
    Interval between running evaluation on validation set.
    """

    split: str = "969, 30, 1"
    """
    Comma_separated list of proportions for training, validation, and test split. For example the split 90,5,5 will use 90% of data for training, 5% for validation and 5% for test.
    """

    vocab_file: str = None
    """
    Path to the vocab file.
    """

    merge_file: str = None
    """
    Path to the BPE merge file.
    """

    num_workers: int = 2
    """
    Dataloader number of workers.
    """

    exit_interval: int = None
    """
    Exit the program after the iteration is divisible by this value.
    """

    attention_dropout: float = 0.1
    """
    Post attention dropout probability.
    """

    hidden_dropout: float = 0.1
    """
    Dropout probability for hidden state transformer.
    """

    weight_decay: float = 0.01
    """
    Weight decay coefficient for L2 regularization.
    """

    checkpoint_activations: bool = False
    """
    Checkpoint activation to allow for training with larger models, sequences, and batch sizes.
    """

    checkpoint_num_layers: int = 1
    """
    Chunk size (number of layers) for checkpointing.
    """

    distribute_checkpointed_activations: bool = False
    """
    If set, distribute checkpointed activations across model parallel group.
    """

    deepspeed_activation_checkpointing: bool = False
    """
    Uses activation checkpointing from deepspeed
    """
    
    contiguous_checkpointing: bool = False
    """
    Contiguous memory checkpointing for activations.
    """
    
    checkpoint_in_cpu: bool = False
    """
    Move the activation checkpoints to CPU.
    """
    
    synchronize_each_layer: bool = False
    """
    does a synchronize at the beginning and end of each checkpointed layer.
    """
    
    profile_backward: bool = False
    """
    Enables backward pass profiling for checkpointed layers.
    """
    
    partition_activations: bool = False
    """
    Partition Activations across GPUs before checkpointing.
    """

    gas: int = None
    """gradient_accumulation_steps""" #TODO this is a duplicate, remove?


    clip_grad: float = None
    """
    Gradient clipping based on global L2 norm.
    """

    hysteresis: int = 2
    """
    hysteresis for dynamic loss scaling
    """

    dynamic_loss_scale: bool = None
    """
    flag indicating whether dynamic loss scale is used
    """

    loss_scale: float = None
    """
    Static loss scaling, positive power of 2
    values can improve fp16 convergence. If None, dynamic loss scaling is used.
    """

    loss_scale_window: float = 1000.0
    """
    Window over which to raise/lower dynamic scale.
    """

    min_scale: float = 1.0
    """
    Minimum loss scale for dynamic loss scale.
    """