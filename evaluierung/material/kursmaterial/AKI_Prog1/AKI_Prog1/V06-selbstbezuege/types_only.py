#Automatically extracted from ./06-selbstbezuege.md on 2026-10-26 17:29:37.008152 UTC



#--------------------------------
#Flüsse in Python zusammengefasst
#--------------------------------

#[./06-selbstbezuege.md:136]
from wypp import *

@record
class Creek:
    origin: str
    name: str

@record
class Confluence:
    location: str
    mainStem: RiverSection
    tributary: RiverSection

type RiverSection = Union[Creek, Confluence]

