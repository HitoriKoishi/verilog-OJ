module ref_module(
    input wire clk,
    input wire d,
    output reg q
);
    // D触发器的功能实现
    always @(posedge clk) begin
        q <= d;  // 在时钟上升沿，输出等于输入
    end
endmodule