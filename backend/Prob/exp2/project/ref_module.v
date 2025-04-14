
module nand_gate_3(
    input a,
    input b,
    input c,
    output r
);
    assign r = ~(a & b &c);
endmodule