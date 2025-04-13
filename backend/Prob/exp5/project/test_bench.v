`timescale 1ns / 1ps
module test_bench();
    reg 	d, clk;
    wire	q;

    d_ff d_ff(
            .d(d), 
            .clk(clk), 
            .q(q)
            );
    initial begin
        d <= 0;
        clk <= 0; 
        #100 $stop;
    end
    always #5  clk = ~clk;
    always #10 d <= d+1; 
endmodule