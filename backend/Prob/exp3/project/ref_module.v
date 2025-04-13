
module three_vote
(
    input a,
    input b,
    input c,
    output r
    );
    assign r=a&b|a&c|b&c; //  r=ab+ac+bc 
endmodule