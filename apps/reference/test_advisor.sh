rm -rf annotations.advidb2 config/ e000/ reference.advixeproj report.html
prun -np 1 advisor --collect=roofline --project-dir=. -- ./gol.o 1920 1080 500 0 0 
advisor --report=roofline --data-type=int --project-dir=. --report-output=./report.html
