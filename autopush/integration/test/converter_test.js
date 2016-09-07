describe("Color Code Converter", function() {
  describe("RGB to Hex conversion", function() {
    it("converts the basic colors", function(done) {
      var redHex   = converter.rgbToHex(255, 0, 0);
      var greenHex = converter.rgbToHex(0, 255, 0);
      var blueHex  = converter.rgbToHex(0, 0, 255);

      chai.expect(redHex).to.equal("ff0000");
      chai.expect(greenHex).to.equal("00ff00");
      chai.expect(blueHex).to.equal("0000ff");

      setTimeout(done, 2000);
    });
  });

  describe("Hex to RGB conversion", function() {
    it("converts the basic colors", function(done) {
      var red   = converter.hexToRgb("ff0000");
      var green = converter.hexToRgb("00ff00");
      var blue  = converter.hexToRgb("0000ff");

      chai.expect(red).to.deep.equal([255, 0, 0]);
      chai.expect(green).to.deep.equal([0, 255, 0]);
      chai.expect(blue).to.deep.equal([0, 0, 255]);

      setTimeout(done, 2000);
    });
  });
});
