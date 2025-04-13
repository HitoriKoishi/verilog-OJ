
module nand_gate_3(
    input a,
    input b,
    input c,
    output y
);
    assign y = ~(a & b &c);
endmodule