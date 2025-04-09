set StdArithNoWarnings 1
set NumericStdNoWarnings 1

quit -sim
if {[file exists work]} {
  file delete -force work 
}
vlib work
vmap work work

set WORK_DIR        "work"
set LOG_FILE        "simulation.log"
set TB_MODULE       "test_bench"
set SIM_FILE_LIST   "sim_file_list.f"
set TIMEOUT_NS      1000

if {[file exists $LOG_FILE]} { file delete $LOG_FILE }
if {[file exists $WORK_DIR]} { file delete -force $WORK_DIR }       
transcript file $LOG_FILE
transcript on

vlib $WORK_DIR
vmap work $WORK_DIR

if {[catch {
    vlog -work work -mfcu -incr -suppress 3485 -suppress 8683 -suppress 2902 -f $SIM_FILE_LIST
} error_msg]} {
    echo "** ERROR: Compilation failed - $error_msg"
    transcript off
    exit 1   
}

if {[catch {
    vsim -quiet -c -voptargs="+acc" +nowarn1 -L work $TB_MODULE
} error_msg]} {
    echo "** ERROR: Simulation load failed - $error_msg"
    transcript off
    exit 1
}

set start_time [now]
set has_error 0

if {[catch {
    run -all
} error_msg]} {
    set has_error 1
    echo "** ERROR: Simulation runtime error - $error_msg"
}

run ${TIMEOUT_NS}ns
if {[now] < $TIMEOUT_NS} {
    set has_error 1
    echo "** ERROR: Simulation did not finish (missing $finish?)"
}

set current_time [now]
if {[expr $current_time - $start_time] > $TIMEOUT_NS} {
    set has_error 1
    echo "** ERROR: Simulation timeout after $TIMEOUT_NS ns"
}

if {$has_error} {
    file delete $WAVE_FILE
    transcript off
    exit 1
} else {
    transcript off
    exit 0
}
quit -force