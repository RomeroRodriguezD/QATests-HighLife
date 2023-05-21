# QA Tests - High Life Shop - Allure UI
Automated tests and reports performed on "https://highlifeshop.com/speedbird-cafe" using Selenium, Behave and Allure.

# Pre-requisites

  -Having Behave module installed on our project environment.
  -Having Allure behave installed on our project environment.

# Run Allure-Behave reporting algorithm

To run Allure-Behave reporting algorithm we should first run this command on terminal, inside our project folder:

   <i>behave -f allure_behave.formatter:AllureFormatter -o reports/ features </i>
   
# This will perform our tests and create JSON reports

![image](https://github.com/RomeroRodriguezD/QATests-HighLife/assets/105886661/e50a33d2-fccd-4afc-acf9-beebcbfd65c6)

# Once we got the reports, we could set up the UI from Allure on our localhost and get interesting insights

Set up the UI with this command:

<i> allure serve reports/ </i>

![image](https://github.com/RomeroRodriguezD/QATests-HighLife/assets/105886661/a7bc627f-596e-4349-a675-88f6f706084e)

# Now we can check our test data through the URL served

<b>-Overview</b>

![image](https://github.com/RomeroRodriguezD/QATests-HighLife/assets/105886661/8f4cf171-9f88-4371-9715-de4738744ee2)

<b>-Categories</b>

![image](https://github.com/RomeroRodriguezD/QATests-HighLife/assets/105886661/22c067e1-5e24-4f6e-af46-788357347a77)

<b>-Suites</b>

![image](https://github.com/RomeroRodriguezD/QATests-HighLife/assets/105886661/7b3d22a9-ad10-40d3-96fb-7db37ce91fc1)

<b>-Graphs</b>

![image](https://github.com/RomeroRodriguezD/QATests-HighLife/assets/105886661/792e5686-b78b-4420-b4d6-7def0923b287)

<b>-Behaviors</b>

![image](https://github.com/RomeroRodriguezD/QATests-HighLife/assets/105886661/ff9a755f-4ea4-4110-8f39-6ab146f6ed53)

<b> And you can download the reports by clicking on this export option: </b>

![image](https://github.com/RomeroRodriguezD/QATests-HighLife/assets/105886661/a00dd96a-b2fd-4975-a639-dc3e8003a3c3)
