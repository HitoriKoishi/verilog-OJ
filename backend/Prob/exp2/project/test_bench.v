`timescale 1ns/1ps
module test_bench();
    reg a, b, c;
    wire y;
    nand_gate_3 nand_gate_3(.a(a), .b(b), .c(c), .y(y));
    initial begin
            a <= 0; b <= 0; c <= 0;
        #10 a <= 0; b <= 0; c <= 1;
        #10 a <= 0; b <= 1; c <= 0;
        #10 a <= 0; b <= 1; c <= 1;
        #10 a <= 1; b <= 0; c <= 0;
        #10 a <= 1; b <= 0; c <= 1;
        #10 a <= 1; b <= 1; c <= 1;
        #10 $stop;
    end
endmodule