
`timescale 1ns / 1ps
module test_bench();
    reg a, b, c;
    wire r;
    three_vote uut(a, b, c, r);
    initial begin
        a = 0; b = 0; c = 0;
    end
    always #10{a,b,c} = {a,b,c} + 1;
endmodule