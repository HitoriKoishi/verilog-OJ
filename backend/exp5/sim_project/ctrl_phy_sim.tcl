set NO_ERROR            0
set ERROR_COMPILE_FAIL  1
set ERROR_SIM_LOAD_FAIL 2
set ERROR_SIM_RUN_FAIL  3
set ERROR_SIM_TIMEOUT   4
set ERROR_MISMATCH      5
set ERROR_TCL_NOT_FOUND 6

set StdArithNoWarnings 1
set NumericStdNoWarnings 1

set WORK_DIR        "work"
set LOG_FILE        "simulation.log"
set TB_MODULE       "test_bench"
set SIM_FILE_LIST   "sim_file_list.f"
set TIMEOUT_NS      10000
set mismatch_detected 0

if {[file exists $LOG_FILE]} { file delete $LOG_FILE }
if {[file exists $WORK_DIR]} { file delete -force $WORK_DIR }
transcript file $LOG_FILE
transcript on

vlib $WORK_DIR
vmap work $WORK_DIR

proc exit_sim {x} {
    global WORK_DIR
    transcript off
    if {[file exists transcript]} { file delete transcript }
    if {[file exists modelsim.ini]} { file delete modelsim.ini }
    if {[file exists $WORK_DIR]} { file delete -force $WORK_DIR }
    quit -force -code $x
}

if {[catch {
    vlog -work work -mfcu -incr\
    -suppress 3485\
    -suppress 8683\
    -suppress 2902\
    -suppress 2083\
    -f $SIM_FILE_LIST
} error_msg]} {
    #vlog编译错误
    echo "** ERROR: Compilation failed - $error_msg"
    exit_sim $ERROR_COMPILE_FAIL
}

if {[catch {
    vsim -quiet -c -voptargs="+acc" +nowarn1 -L work $TB_MODULE
} error_msg]} {
    #vsim仿真加载错误
    echo "** ERROR: Simulation load failed - $error_msg"
    exit_sim $ERROR_SIM_LOAD_FAIL
}

#把 -fast去掉就好了？
when {mismatch != 0} { set mismatch_detected 1 }

if {[catch {
    run -all
} error_msg]} {
    #仿真执行时发生错误
    echo "** ERROR: Simulation runtime error - $error_msg"
    exit_sim $ERROR_SIM_RUN_FAIL
}

# 检查不匹配
if {$mismatch_detected} {
    echo "** ERROR: Output mismatch with reference"
    exit_sim $ERROR_MISMATCH
} else {
    echo "INFO: Simulation PASSED"
    exit_sim $NO_ERROR
}