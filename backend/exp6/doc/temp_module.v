
module counter_10(
    input clk,
    input rst,
    output [3:0] count
    );
    reg [3:0] q;
    assign count = q;

endmodule