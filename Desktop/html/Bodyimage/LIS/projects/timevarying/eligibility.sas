*****************************************************************************************************************;
* E L I G I B I L I T Y . S A S                          
*
* Turns raw state change data into event times and eligible times for various events such as remission, relapse, etc.
*
* EPQ 7/6/2010
****************************************************************************************************************;
libname this '.';

proc format;
value $state 'IE_FC'="In_episode, full_criteria" 
            'IE_NFC'="In episode, not full criteria"
            'NIE_NFC'="Not in episode, not full criteria"
            'NIE_NP'="Not in episode, not present";

%macro pdfopen(ds=);
run;
ods pdf file="ODS/&ds._&SYSDATE..pdf";
run;
%mend pdfopen;

%macro pdfclose;
run;
ods pdf close;
run;
%mend pdfclose;

%macro rd_state(disorder=BDD);
filename bdd "data/STATE_&disorder..txt";
data 
  eligible (keep=ID ID_num disorder event week week_eligible)
  censor (keep=ID ID_num disorder intake_state maxweek)
  events (keep=ID ID_num disorder event week tostate);
length disorder $ 8 event $ 25;
infile bdd missover length=l;

length intake_state fromstate tostate week_s $ 8 line $ 200 week ID_num 8;
retain fromstate tostate;

input line $varying. l;

retain disorder "&disorder";

put line=;


if index(line,'SS:')>0 then do;                *pick up SCD variables;

if disorder='BDD' then do;
   scda102=input(scan(line,3," "),1.);
   scda104=input(scan(line,6," "),1.);
   scda106=.;
   retain scda102 scda104 scda106;
   if scda102=1 and scda104=2 then intake_state='IE_FC'; 
   if scda102=1 and scda104=3 then intake_state='IE_NFC'; 
                              else intake_state='NIE_NFC';
   end;

if disorder='MDD' then do;
   scda16=input(scan(line,3," "),1.);
   scda18=input(scan(line,5," "),1.);
   retain scda16 scda18;
   end;
   delete;
   end;

if index(line,'ID=')>0 then do;                *pick up ID;
   ID=input(scan(line,2,"="),$5.);
   ID_num=substr(ID,1,length(ID)-2);
   tostate="START";
   retain ID_num ID;
   delete;
   end;

if index(line,'Max')>0 then do;                *pick up max week;
   maxweek=input(scan(line,3," "),5.);
   output censor;
   retain maxweek;
   end;

if index(line,'Initial')>0 then do;
   intake_state=scan(line,3," ");
   if intake_state=:"state" then intake_state=scan(line,4," ");
   week=0;
   week_eligible=0;
   if intake_state=:"IE_FC" then do; event="remission"; output eligible; event="partial remission"; output eligible; end;
   else if intake_state=:"IE_NFC" then do; event="remission"; output eligible; event="partial relapse"; output eligible; end;
   else do;
      if intake_state="NIE_NP" then do; event="relapse"; output eligible; event="partial onset"; output eligible; end;
      if intake_state="NIE_NFC" then do; event="relapse"; output eligible; event="partial improve"; output eligible;end;
   end;
   retain intake_state;
   delete;
end;

if index(line,'STATE CHANGE')>0 then do;
   fromstate=scan(line,4," ");
   tostate=scan(line,6," ");
   k=index(line,"WEEK")+4;
   week_s=substr(line,k);
   week=week_s; *convert to numeric;
   week_eligible=week;
   if fromstate="IE_FC" then do;
      if tostate="IE_NFC" then do;  
            event="partial remission"; output events;
            event="partial relapse";   output eligible; 
            end;
      if tostate="NIE_NP" then do;
            event="remission";         output events;  
            event="relapse";           output eligible; 
            event="partial onset";   output eligible; 
            end;
      end;
   if fromstate="IE_NFC" then do;
      if tostate="IE_FC" then do;
            event="partial relapse";     output events;   
            event="partial remission";   output eligible;
            *event="remission";          *output eligible; *already eligible;  
            end;
      if tostate="NIE_NP" then do;  
            event="remission";         output events;
            event="relapse";           output eligible; 
            event="partial onset";   output eligible; 
            end;
      end;
   if fromstate=:"NIE_NFC" then do;
      if tostate=:"IE_FC" then do; 
            event="relapse";             output events;
            event="remission";           output eligible; 
            event="partial remission";   output eligible; 
            end;
      if tostate=:"NIE_NP" then do;  
            event="partial improve";     output events;
            *event="relapse";            *output eligible; 
            event="partial onset";       output eligible; 
            end;
      end;
   if fromstate=:"NIE_NP" then do;
      if tostate=:"IE_FC" then do; 
            event="relapse";             output events;
            event="remission";           output eligible; 
            event="partial remission";   output eligible; 
            end;
      if tostate=:"NIE_NFC" then do;  
            event="partial onset";    output events;        *partial onset event: not in episode NP to NFC;
            event="partial improve";  output eligible;             *eligible for partial improve: NFC to NP;
                                                                  *relapse eligibility already noted under NIE_NP;  
            end;
      end;
end;
title "5/17/2010 Data Dump";
run;

data all;
set events(in=inevt) eligible(in=inel);
if inel then type="eligible";
if inevt then type="event";

proc sort data=all;    by ID_num ID week;
proc sort data=censor; by ID_num ID;

data all2; 
merge all censor; by ID_num ID;
if ID='' then delete;
*proc print; 
*by id;
title 'combined';
%mend rd_state;
%rd_state(disorder=BDD);
data all_evt;
set all2;
%rd_state(disorder=MDD);
data all_evt;
set all_evt all2;
by ID_num ID;
%rd_state(disorder=OCD);
data all_evt;
set all_evt all2;
by ID_num ID;
if length(ID)<3 then delete;
%rd_state(disorder=SOC);
data all_evt;
set all_evt all2;
by ID_num ID;
proc sort data=all_evt;
by disorder ID_num ID week;

data this.all_evt; set all_evt;

%pdfopen(ds=consolidated_events);
proc print data=this.all_evt(where=(disorder="BDD"));
by disorder ID_num ID intake_state;
title2 "Consolidated_Events_List";
%pdfclose;

%pdfopen(ds=event_counts);
proc freq data=this.all_evt(where=(disorder="BDD"));
tables event*type;
title2 "Consolidated Event Counts";
%pdfclose;
endsas;
