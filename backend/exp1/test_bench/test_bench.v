`timescale 1ns/1ps
module test_bench(); //test_bench模块名不可更改，tcl脚本需要识别
reg clk;
reg rstn;
reg refrence_in;
wire your_out, refrence_out;
wire mismatch = (refrence_out !== your_out); //强判断，x或z也会判断是否相等
//mismatch信号不可省略，mismatch的逻辑由test_bench决定，tcl脚本识别mismatch信号，如果在仿真过程中不为0则波形不匹配。

initial clk = 0;
always #10 clk = ~clk;

initial begin
    $dumpfile ("waveform.vcd"); //生成波形文件
    $dumpvars (0,test_bench.clk,test_bench.rstn,test_bench.refrence_in,test_bench.your_out,test_bench.refrence_out,test_bench.mismatch); //自行按顺序添加需要记录的波形
    rstn = 1;
    refrence_in = 0;
    #30 $dumpon; //开始记录波形
    #10 rstn = 0;
    #50 rstn = 1;
    #25 refrence_in = 1;
    #25 refrence_in = 0;
    #25 refrence_in = 1;
    #25 refrence_in = 0;
    #25 $dumpoff; //结束记录波形
    $stop(); //必须使用stop停止仿真，使用finish会强制关闭进程
end


xor_trigger user_module_inst(
    .clk    (clk        ),
    .rstn   (rstn       ),
    .in     (refrence_in),
    .out    (your_out   )
);
ref_module ref_module_inst(
    .clk    (clk         ),
    .rstn   (rstn        ),
    .in     (refrence_in ),
    .out    (refrence_out)
);

endmodule //test_bencch
