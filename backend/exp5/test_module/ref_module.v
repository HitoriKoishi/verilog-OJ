
module d_ff(
    input d,
    input clk,
    output q
    );
    reg	q; 
    always @(posedge clk)
    begin
        q <= d;
    end
endmodule