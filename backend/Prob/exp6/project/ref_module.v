module ref_module(
    input wire clk,
    input wire rstn,
    output reg [3:0] count
);
    // 十进制计数器的功能实现
    always @(posedge clk or negedge rstn) begin
        if (!rstn)  // 异步复位
            count <= 4'b0000;
        else if (count == 4'd9)  // 计数到9时清零
            count <= 4'b0000;
        else  // 正常计数
            count <= count + 1'b1;
    end
endmodule