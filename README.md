# LoanRepaymentCalculator
Python Utility for calculating repayment for a simple loan.

LoanCalculator.py - Module includes calculation functions. Executing Module Mainline (no args necessary) with executes a demonstration test case. 

LoanCalculatorGUI.py - Basic TkInter UI for accessing functionality in LoanCalculator.py. Depends on LoanCalculator.py.

LoanCalculationServer.py - Basic Flask Server to make Api available. It includes a simple Html template. Usage: to start, use "flask --app LoanCalculationServer run --debug"

calcsite.py - FastApi implementation of pythonserver. Angular UI is setup to call this server. Start this server (after installing the necessary modules using pip3) with this command "fastapi dev ./calcsite.py".

I added Angular FrontEnd in ./angularUI folder, should be able to start in that directory with ng serve. It requires LoanCalculatorServer.py to be running.