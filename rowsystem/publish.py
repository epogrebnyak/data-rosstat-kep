class Publisher():
    
    def write_xl(self):
       print(1)
    
    def write_csv(self):
       print(1)
    
    def varnames_md(self):
       print(1)
       
    def write_monthly_pdf(self):
       print(1)
       
    def write_monthly_png(self):
       self._write_png_images()
       self._write_png_showcase_markdownfile()
       
    def _write_png_images(self):
       print(2)
       
    def _write_png_showcase_markdownfile(self):
       print(2)    
       
    def publish(self):
       self.write_xl()
       self.write_csv()
       self.varnames_md()
       self.write_monthly_pdf()
       self.write_monthly_png()
       