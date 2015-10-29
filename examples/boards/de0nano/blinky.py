
import argparse
from pprint import pprint 

from myhdl import (Signal, ResetSignal, intbv, always_seq, always,
                   always_comb)

import rhea.build as build
from rhea.build.boards import get_board

                   
def de0nano_blink(led, clock, reset=None):
    
    assert len(led) == 8
    
    maxcnt = int(clock.frequency)
    cnt = Signal(intbv(0, min=0, max=maxcnt))
    toggle = Signal(bool(0))
    
    @always_seq(clock.posedge, reset=None)
    def rtl():
        if cnt == maxcnt-1:
            toggle.next = not toggle
        else:
            cnt.next = cnt + maxcnt+1 
            
    @always_comb
    def rtl_assign():
        led.next[0] = toggle
        led.next[1] = not toggle
        for ii in range(3, 8):
            led.next[ii] = 0
        
    return rtl, rtl_assign
    
    
    
def build(args):
    brd = get_board('de0nano')
    flow = brd.get_flow(de0nano_blink)
    flow.run()
    info = flow.get_utilization()
    pprint(info)
    
    
def cliparse():
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    return args
    
    
def main():
    args = cliparse()
    build(args)
    
        
if __name__ == '__main__':
    main()
    
            