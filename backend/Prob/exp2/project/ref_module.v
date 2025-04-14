module ref_module(
    input wire a,
    input wire b,
    input wire c,
    output wire y
);
    // 使用assign语句实现三输入与非门
    assign y = ~(a & b & c);
    
endmodule