`timescale 1ns/1ps
module test_bench();
reg clk;
reg rstn;
reg refrence_in;
wire your_out, refrence_out;
wire mismath_out = (refrence_out != your_out);

initial clk = 0;
always #10 clk = ~clk;

initial begin
    $dumpfile ("waveform.vcd");
    $dumpvars (0,test_bench.clk,test_bench.rstn,test_bench.refrence_in,test_bench.your_out,test_bench.refrence_out,test_bench.mismath_out);
    rstn = 1;
    refrence_in = 0;
    #30 $dumpon;
    #10 rstn = 0;
    #50 rstn = 1;
    #25 refrence_in = 1;
    #25 refrence_in = 0;
    #25 refrence_in = 1;
    #25 refrence_in = 0;
    #25 $dumpoff;
    $finish();
end


user_module user_module_inst(
    .clk    (clk        ),
    .rstn   (rstn       ),
    .in     (refrence_in),
    .out    (your_out   )
);
ref_module ref_module_inst(
    .clk    (clk         ),
    .rstn   (rstn       ),
    .in     (refrence_in ),
    .out    (refrence_out)
);

endmodule //test_bencch
