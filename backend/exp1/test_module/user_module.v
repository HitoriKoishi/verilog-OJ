module xor_trigger (
    input clk,
    input rstn,
    input in, 
    output reg out
);
always@(posedge clk or negedge rstn) begin
    if(~rstn) out <= 0;
<<<<<<< Updated upstream
	else out <= in ^ out;    
=======
    else out <= in ^ out;    
>>>>>>> Stashed changes
end
endmodule