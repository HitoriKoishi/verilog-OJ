module ref_module(
    input wire a,
    input wire b,
    input wire c,
    output wire r
);
    // 使用最简与或表达式实现三人表决器
    assign r = (a & b) | (a & c) | (b & c);
endmodule