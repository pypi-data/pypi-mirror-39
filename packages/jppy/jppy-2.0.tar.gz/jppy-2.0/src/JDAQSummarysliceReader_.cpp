#include <string>
#include <vector>
#include "common.h"
#include "JLang/JObjectReader.hh"
#include "JLang/JSinglePointer.hh"
#include "JDAQ/JDAQSummaryslice.hh"
#include "JDAQ/JDAQEvaluator.hh"
#include "JSupport/JTreeScanner.hh"
#include "JSupport/JAutoTreeScanner.hh"
#include "JROOT/JROOTClassSelector.hh"
#include "JSupport/JSupport.hh"
#include "JLang/JObjectMultiplexer.hh"
#include "JDAQSummarysliceReader.h"

using namespace KM3NETDAQ ;     // for JDAQSummaryslice
using namespace JSUPPORT;       // for JFileScanner and JTreeScanner
using namespace JLANG;

namespace jppy {

    JAutoTreeScanner<JDAQSummaryslice> zmap;
    JTreeScannerInterface<JDAQSummaryslice>* ps;

    std::string _filename;
    KM3NETDAQ::JDAQSummaryslice* summaryslice;
    JDAQSummaryslice::const_iterator superframe;
    int summaryslice_idx = 0;
    int superframe_idx = 0;
    int n_summaryslices = 0;
    int n_frames = 0;
    int n_hits = 0;
    std::map<int, int> frame_index_map;

    JDAQSummarysliceReader::JDAQSummarysliceReader() {}

    JDAQSummarysliceReader::JDAQSummarysliceReader(char* filename) {
        _filename = std::string(filename);

        zmap = JType<JDAQSummarysliceType_t>();

        ps = zmap[_stream];
        if(!zmap[_stream].is_valid()) {
            std::cout << "Stream '" << stream << "' not found!" << std::endl;
        } else {
            ps->configure(_filename);
            n_summaryslices = ps->getEntries();
            initTreeScanner();
        }
    }

    void JDAQSummarysliceReader::initTreeScanner() {
        std::cout << "Initialising frame index lookup, this may take a few seconds." << std::endl;
        for(int i=0; i < n_summaryslices; i++) {
            JDAQSummaryslice* summaryslice = ps->getEntry(i);
            frame_index_map[summaryslice->getFrameIndex()] = i;
        }
        std::cout << n_summaryslices << " summaryslices indexed." << std::endl;
    }

    void JDAQSummarysliceReader::retrieveSummaryslice(int index) {
        summaryslice = ps->getEntry(index);
        superframe = summaryslice->begin();
        n_frames = 0;
        n_hits = 0;
        for (JDAQSummaryslice::const_iterator frame = summaryslice->begin();
             frame != summaryslice->end();
             ++frame) {
            n_hits += frame->size();
            n_frames += 1;
        }
    }

    void JDAQSummarysliceReader::retrieveSummarysliceAtFrameIndex(int frame_index) {
        int i = frame_index_map[frame_index];
        retrieveSummaryslice(i);
    }

    int JDAQSummarysliceReader::getNumberOfSummaryslices() {
        return n_summaryslices;
    }

    int JDAQSummarysliceReader::getNumberOfFrames() {
        return n_frames;
    }
    int JDAQSummarysliceReader::getNumberOfHits() {
        return n_hits;
    }

    int JDAQSummarysliceReader::getFrameIndex() {
        return superframe->getFrameIndex();
    }

    int JDAQSummarysliceReader::getModuleID() {
        return superframe->getModuleID();
    }

    int JDAQSummarysliceReader::getUTCSeconds() {
        return superframe->getSummarysliceStart().getUTCseconds();
    }

    int JDAQSummarysliceReader::getUTCNanoseconds() {
        return superframe->getSummarysliceStart().getUTC16nanosecondcycles() * 16;
    }

    int JDAQSummarysliceReader::getUDPNumberOfReceivedPackets() {
        return superframe->getUDPNumberOfReceivedPackets();
    }

    int JDAQSummarysliceReader::getUDPMaximalSequenceNumber() {
        return superframe->getUDPMaximalSequenceNumber();
    }

    bool JDAQSummarysliceReader::hasUDPTrailer() {
        return superframe->hasUDPTrailer();
    }

    bool JDAQSummarysliceReader::testWhiteRabbitStatus() {
        return superframe->testWhiteRabbitStatus();
    }

    bool JDAQSummarysliceReader::testHighRateVeto() {
        return superframe->testHighRateVeto();
    }

    bool JDAQSummarysliceReader::testFIFOStatus() {
        return superframe->testFIFOStatus();
    }

    void JDAQSummarysliceReader::getHits(int* channel_ids,
                                      int* dom_ids,
                                      int* times,
                                      int* tots) {
        JDAQSummaryslice::const_iterator sf_it = summaryslice->begin();

        int hit_idx = 0;
        for(int frame_idx=0; frame_idx < n_frames; frame_idx++) {
            for (JDAQSuperFrame::const_iterator hit = sf_it->begin(); hit != sf_it->end(); ++hit ) {
                channel_ids[hit_idx] = static_cast<int>(hit->getPMT());
                dom_ids[hit_idx] = sf_it->getModuleID();
                times[hit_idx] = hit->getT();
                tots[hit_idx] = static_cast<int>(hit->getToT());
                hit_idx += 1;
            }
            sf_it += 1;
        }
    }
}
