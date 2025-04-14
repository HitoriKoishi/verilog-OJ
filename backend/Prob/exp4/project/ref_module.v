module ref_module(
    input wire clk,
    input wire rst,
    input wire j,
    input wire k,
    output reg q
);
    // JK触发器的功能实现
    always @(posedge clk or posedge rst) begin
        if (rst)  // 异步复位
            q <= 1'b0;
        else
            case ({j,k})
                2'b00: q <= q;      // 保持
                2'b01: q <= 1'b0;   // 置0
                2'b10: q <= 1'b1;   // 置1
                2'b11: q <= ~q;     // 翻转
            endcase
    end
endmodule