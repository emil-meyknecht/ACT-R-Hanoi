#################### Model fo agent solving game of Hanoi ###################

# this model uses the contents of DM(declaritive memory) to decide what to do next
# It has a motor model that can act following the instruction in the DM 

import ccm      
log=ccm.log()   

from ccm.lib.actr import *  

class Hanoi(ccm.Model): #environment
    B1 = ccm.Model(isa ='B1', location='A')
    B2 = ccm.Model(isa ='B2', location='A')
    B3 = ccm.Model(isa ='B3', location='A')

class MotorModule(ccm.Model): # motor module
    def move(self, block, location):
        if block == 'B1':
            print "move", self.parent.parent.B1.isa,"from", self.parent.parent.B1.location, "to", location
            self.parent.parent.B1.location = location
        if block == 'B2':
            print "move", self.parent.parent.B1.isa,"from", self.parent.parent.B2.location, "to", location
            self.parent.parent.B2.location = location
        if block == 'B3':
            print "move",self.parent.parent.B1.isa ,"from", self.parent.parent.B3.location, "to", location
            self.parent.parent.B3.location = location
  
class MyAgent(ACTR):# create an act-r agent
    focus=Buffer()
    DMbuffer=Buffer()                           # create a buffer for the declarative memory (henceforth DM)
    DM=Memory(DMbuffer)                         # create DM and connect it to its buffer 
    motor=MotorModule()
    
    def init():                                             
        DM.add ('cue:start step:step1_B1_C')                     
        DM.add ('cue:step1_B1_C step:step2_B2_B')
        DM.add ('cue:step2_B2_B step:step3_B1_B')
        DM.add ('cue:step3_B1_B step:step4_B3_C')
        DM.add ('cue:step4_B3_C step:step5_B1_A')
        DM.add ('cue:step5_B1_A step:step6_B2_C')
        DM.add ('cue:step6_B2_C step:step7_B1_C')
        DM.add ('cue:step7_B1_C step:finished')
        DM.add ('cue:finished step:stop')
        focus.set('begin')
    
    def start_game(focus='begin'):
        print 'start with the game'  
        DM.request('cue:start step:?') 
        focus.set('remember')
   
    def remember_steps(focus='remember', DMbuffer='cue:?cue!finished step:?step',DM='busy:False'):
        if step != 'finished':
            nr, block, location = step.split('_')
            print 'remember', nr, ': move block',block, 'to location ', location
            motor.move(block,location)
        DM.request('cue:?step step:?')   

    def finished (focus='remember', DMbuffer='cue:finished step:?step'):
        print 'finished'   
        focus.set('stop')
        DMbuffer.clear()
        print "I have solved the game of Hanoi"              

    def stop_production(focus='stop'):
        self.stop()

tim=MyAgent()                              # name the agent
subway=Hanoi()                     # name the environment
subway.agent=tim                           # put the agent in the environment
ccm.log_everything(subway)                 # print out what happens in the environment

subway.run()                               # run the environment
ccm.finished()                             # stop the environment

