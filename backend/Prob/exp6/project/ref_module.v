module counter_10(
    input clk,
    input rst,
    output [3:0] count
    );
    reg [3:0] q;
    assign count = q;

    always@(posedge clk)
    begin
      if(!rst)
        q <= 0;
      else if(q >= 4'd9)
        q <= 0;
      else
        q <= q + 1;
    end

endmodule