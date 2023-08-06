#include <string>
#include <vector>
#include "common.h"
#include "JLang/JObjectReader.hh"
#include "JLang/JSinglePointer.hh"
#include "JDAQ/JDAQTimeslice.hh"
#include "JDAQ/JDAQEvaluator.hh"
#include "JSupport/JTreeScanner.hh"
#include "JSupport/JAutoTreeScanner.hh"
#include "JROOT/JROOTClassSelector.hh"
#include "JSupport/JSupport.hh"
#include "JLang/JObjectMultiplexer.hh"
#include "JDAQTimesliceReader.h"

using namespace KM3NETDAQ ;     // for JDAQTimeSlice
using namespace JSUPPORT;       // for JFileScanner and JTreeScanner
using namespace JLANG;

namespace jppy {

    JAutoTreeScanner<JDAQTimeslice> zmap;
    JTreeScannerInterface<JDAQTimeslice>* ps;

    std::string _filename;
    std::string _stream;
    KM3NETDAQ::JDAQTimeslice* timeslice;
    JDAQTimeslice::const_iterator superframe;
    int timeslice_idx = 0;
    int superframe_idx = 0;
    int n_timeslices = 0;
    int n_frames = 0;
    int n_hits = 0;
    std::map<int, int> frame_index_map;

    JDAQTimesliceReader::JDAQTimesliceReader() {}

    JDAQTimesliceReader::JDAQTimesliceReader(char* filename, char* stream) {
        _filename = std::string(filename);
        _stream = std::string(stream);

        zmap = JType<JDAQTimesliceTypes_t>();

        std::cout << "Reading " << stream << " stream... " << std::endl;

        ps = zmap[_stream];
        if(!zmap[_stream].is_valid()) {
            std::cout << "Stream '" << stream << "' not found!" << std::endl;
        } else {
            ps->configure(_filename);
            n_timeslices = ps->getEntries();
            initTreeScanner();
        }
    }

    void JDAQTimesliceReader::initTreeScanner() {
        std::cout << "Initialising frame index lookup, this may take a few seconds." << std::endl;
        for(int i=0; i < n_timeslices; i++) {
            JDAQTimeslice* timeslice = ps->getEntry(i);
            frame_index_map[timeslice->getFrameIndex()] = i;
        }
        std::cout << n_timeslices << " timeslices indexed." << std::endl;
    }

    void JDAQTimesliceReader::retrieveTimeslice(int index) {
        timeslice = ps->getEntry(index);
        superframe = timeslice->begin();
        n_frames = 0;
        n_hits = 0;
        for (JDAQTimeslice::const_iterator frame = timeslice->begin();
             frame != timeslice->end();
             ++frame) {
            n_hits += frame->size();
            n_frames += 1;
        }
    }

    void JDAQTimesliceReader::retrieveTimesliceAtFrameIndex(int frame_index) {
        int i = frame_index_map[frame_index];
        retrieveTimeslice(i);
    }

    int JDAQTimesliceReader::getNumberOfTimeslices() {
        return n_timeslices;
    }

    int JDAQTimesliceReader::getNumberOfFrames() {
        return n_frames;
    }
    int JDAQTimesliceReader::getNumberOfHits() {
        return n_hits;
    }

    int JDAQTimesliceReader::getFrameIndex() {
        return superframe->getFrameIndex();
    }

    int JDAQTimesliceReader::getModuleID() {
        return superframe->getModuleID();
    }

    int JDAQTimesliceReader::getUTCSeconds() {
        return superframe->getTimesliceStart().getUTCseconds();
    }

    int JDAQTimesliceReader::getUTCNanoseconds() {
        return superframe->getTimesliceStart().getUTC16nanosecondcycles() * 16;
    }

    int JDAQTimesliceReader::getUDPNumberOfReceivedPackets() {
        return superframe->getUDPNumberOfReceivedPackets();
    }

    int JDAQTimesliceReader::getUDPMaximalSequenceNumber() {
        return superframe->getUDPMaximalSequenceNumber();
    }

    bool JDAQTimesliceReader::hasUDPTrailer() {
        return superframe->hasUDPTrailer();
    }

    bool JDAQTimesliceReader::testWhiteRabbitStatus() {
        return superframe->testWhiteRabbitStatus();
    }

    bool JDAQTimesliceReader::testHighRateVeto() {
        return superframe->testHighRateVeto();
    }

    bool JDAQTimesliceReader::testFIFOStatus() {
        return superframe->testFIFOStatus();
    }

    void JDAQTimesliceReader::getHits(int* channel_ids,
                                      int* dom_ids,
                                      int* times,
                                      int* tots) {
        JDAQTimeslice::const_iterator sf_it = timeslice->begin();

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
