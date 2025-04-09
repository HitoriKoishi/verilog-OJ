module user_module (
    input clk,
    input rstn,
    input in, 
    output reg out
);
always@(posedge clk or negedge rstn) begin
    if(~rstn) out <= 0;
	else out <= in ^ out;    
end
endmodule