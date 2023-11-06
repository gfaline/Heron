# Heron

This code was run on MacOS, with the M1 chip, running Ventura.

To begin:
pip install -r requirements.txt

Identify Recurring Transactions 
- For the scope of this project, periodicity is daily, weekly, monthly, or yearly
  - They can have the same price or similar name
  - +- 30% of time (So in a week, we can be off by a day or two)
  - A period must be at least three times
- Longest common name can be used for descriptors
  - This will notably allow for people to create recurring expenses that are named wildly different terms even at the same cadence
  - I will try to use this to find a common descriptor to name the expense
  - This also means that if something is recurring but most of the descriptor is different, it will not flag.

To think about:
- Do all recurring transaction happen at the same cadence: Will company lunch always be 7 days apart, will any weeks be missed
- What if the price of a subscription changes? Should it be included with the prior lump of recurring or added to a new one, how is that labeled?
  - For the purpose of this, assume the price must be the same
- Training data is always useful for testing accuracy, but that allows for overfitting. Measuring real world accuracy would likely involve manual labeling or possibly creative data generation
- Material Impact may involve asking customers upon signup how much they spend on each period basis. Then analyzing the difference. There can also be a survey later to try to assess impact or change in recurring expenses
- 