/**
   This c++ scrip validates the output made by its python counterpart test_fitreader.py. They should give
   the same result!. Of course you can avoid this script to make this simple plot, which can be plotted directly
   from the jpp.root file and the Draw option, nonetheless, this allows to compare how to handle a root file via JPP vs jppy

   To run this one. First load your JPP environment, then run the command line below (you will get a lot of warnings, never mind, this is because of the line below includes **minimal** JPP/AANET libraries)

c++ `root-config --cflags --libs` -I $JPP_DIR/software/ -L $JPP_LIB/ -levtROOT -DVERSION=\"8081\" test_fitreader.cc -o test_fitreader 

Finally run it like ./test_fitreader -i YourInputJppFile.root -o NameFile.root
Then, open NameFile.root and your histogram will be in there. 
*/

#include <string>

#include "JSupport/JFileScanner.hh"
#include "JFit/JEvt.hh"

#include "Jeep/JParser.hh"
#include "Jeep/JMessage.hh"//for FATAL

#include "TH1D.h"

int main(int argc, char **argv)
{  
  //============================= Parser Options
  std::string inputFileName;
  std::string outputFileName;

  try { 
    JParser<> zap("This Plots the Z-dir of the first JFit given by JEvt.");
    
    zap['i'] = make_field(inputFileName);
    zap['o'] = make_field(outputFileName);
    if (zap.read(argc, argv) != 0)
      return 1;
  }
  catch(const std::exception& error) {
    FATAL(error.what() << std::endl);
  }

  TFile *outputfile= new TFile(outputFileName.c_str(),"recreate");  
  TH1D *h_dir_z= new TH1D("h_dir_z","",50,-1,1);
   
  JSUPPORT::JFileScanner<JFIT::JEvt> inputFile(inputFileName.c_str());
  
  while (inputFile.hasNext()) {
    const JFIT::JEvt *jevt = inputFile.next();
       
    if (jevt->empty()) continue;
  
    const JFIT::JFit &firstfit= jevt->at(0);
    const double dir_z= firstfit.getDZ();
    h_dir_z->Fill(dir_z);
  }

  outputfile->Write();
  outputfile->Close();
 
  return 0;
}





