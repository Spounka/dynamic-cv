TEX="/usr/bin/lualatex"

FULL_STACK_ATS_TARGET="Fullstack ats.tex"
FULL_STACK_PRINTABLE="Fullstack CV.tex"

BACKEND_ATS_TARGET="Backend ats.tex"
BACKEND_PRINTABLE="Backend CV.tex"

FRONT_ATS_TARGET="Frontend ats.tex"
FRONT_PRINTABLE="Frontend CV.tex"

BUILD_DIR="$(pwd)/build"



all: fullats fullprintable frontats frontprintable backats backprintable

.PHONY: fullats
fullats:
	mkdir -p $(BUILD_DIR)/fullstack/ats
	cd build/ats
	$(TEX) -output-directory=build/ats --jobname="Nazih_Boudaakkar_Full_Stack_CV" $(FULL_STACK_ATS_TARGET)

.PHONY: fullprintable
fullprintable:
	mkdir -p $(BUILD_DIR)/fullstack/printable
	cd build/printable
	$(TEX) -output-directory=build/printable --jobname="Nazih_Boudaakkar_Full_Stack_CV" $(FULL_STACK_PRINTABLE) 


.PHONY: frontats
fullats:
	mkdir -p $(BUILD_DIR)/frontend/ats
	cd build/ats
	$(TEX) -output-directory=build/ats --jobname="Nazih_Boudaakkar_Frontend_CV" $(FRONT_ATS_TARGET)

.PHONY: frontprintable
fullprintable:
	mkdir -p $(BUILD_DIR)/frontend/printable
	cd build/printable
	$(TEX) -output-directory=build/printable --jobname="Nazih_Boudaakkar_Frontend_CV" $(FRONT_PRINTABLE) 

.PHONY: backats
fullats:
	mkdir -p $(BUILD_DIR)/backend/ats
	cd build/ats
	$(TEX) -output-directory=build/ats --jobname="Nazih_Boudaakkar_Backend_CV" $(BACKEND_ATS_TARGET)

.PHONY: backprintable
fullprintable:
	mkdir -p $(BUILD_DIR)/backend/printable
	cd build/printable
	$(TEX) -output-directory=build/printable --jobname="Nazih_Boudaakkar_Backend_CV" $(BACKEND_PRINTABLE) 


	
.PHONY: clean
clean:
	$(RM) *.gz **/*.gz *.aux **/*.aux *.bbl **/*.bbl *.blg  **/*.blg *.log *.out *.fls *.fdb_latexmk **/*.log **/*.out **/*.fls **/*.fdb_latexmk *.pdf
