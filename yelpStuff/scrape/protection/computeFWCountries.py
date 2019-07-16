# -*- coding: utf-8 -*-
import re

html = '</a><i style="float:right;font-size:16px;padding-top:2px" class="fa fa-bars"></i></td></tr></thead><tbody><tr><td><img src="https://s3.amazonaws.com/images.wpr.com/flags/24/US.png"/></td><td><a href="/countries/united-states-population/">United States</a></td><td>9,372,610 km²</td><td>329,093,110</td><td>0.71%</td></tr><tr><td><img src="https://s3.amazonaws.com/images.wpr.com/flags/24/JP.png"/></td><td><a href="/countries/japan-population/">Japan</a></td><td>377,930 km²</td><td>126,854,745</td><td>-0.26%</td></tr><tr><td><img src="https://s3.amazonaws.com/images.wpr.com/flags/24/TR.png"/></td><td><a href="/countries/turkey-population/">Turkey</a></td><td>783,562 km²</td><td>82,961,805</td><td>1.28%</td></tr><tr><td><img src="https://s3.amazonaws.com/images.wpr.com/flags/24/DE.png"/></td><td><a href="/countries/germany-population/">Germany</a></td><td>357,114 km²</td><td>82,438,639</td><td>0.18%</td></tr><tr><td><img src="https://s3.amazonaws.com/images.wpr.com/flags/24/GB.png"/></td><td><a href="/countries/united-kingdom-population/">United Kingdom</a></td><td>242,900 km²</td><td>66,959,016</td><td>0.58%</td></tr><tr><td><img src="https://s3.amazonaws.com/images.wpr.com/flags/24/FR.png"/></td><td><a href="/countries/france-population/">France</a></td><td>551,695 km²</td><td>65,480,710</td><td>0.38%</td></tr><tr><td><img src="https://s3.amazonaws.com/images.wpr.com/flags/24/IT.png"/></td><td><a href="/countries/italy-population/">Italy</a></td><td>301,336 km²</td><td>59,216,525</td><td>-0.13%</td></tr><tr><td><img src="https://s3.amazonaws.com/images.wpr.com/flags/24/KR.png"/></td><td><a href="/countries/south-korea-population/">South Korea</a></td><td>100,210 km²</td><td>51,339,238</td><td>0.34%</td></tr><tr><td><img src="https://s3.amazonaws.com/images.wpr.com/flags/24/ES.png"/></td><td><a href="/countries/spain-population/">Spain</a></td><td>505,992 km²</td><td>46,441,049</td><td>0.09%</td></tr><tr><td><img src="https://s3.amazonaws.com/images.wpr.com/flags/24/CA.png"/></td><td><a href="/countries/canada-population/">Canada</a></td><td>9,984,670 km²</td><td>37,279,811</td><td>0.88%</td></tr><tr><td><img src="https://s3.amazonaws.com/images.wpr.com/flags/24/AU.png"/></td><td><a href="/countries/australia-population/">Australia</a></td><td>7,692,024 km²</td><td>25,088,636</td><td>1.28%</td></tr><tr><td><img src="https://s3.amazonaws.com/images.wpr.com/flags/24/NL.png"/></td><td><a href="/countries/netherlands-population/">Netherlands</a></td><td>41,850 km²</td><td>17,132,908</td><td>0.28%</td></tr><tr><td><img src="https://s3.amazonaws.com/images.wpr.com/flags/24/BE.png"/></td><td><a href="/countries/belgium-population/">Belgium</a></td><td>30,528 km²</td><td>11,562,784</td><td>0.56%</td></tr><tr><td><img src="https://s3.amazonaws.com/images.wpr.com/flags/24/GR.png"/></td><td><a href="/countries/greece-population/">Greece</a></td><td>131,990 km²</td><td>11,124,603</td><td>-0.16%</td></tr><tr><td><img src="https://s3.amazonaws.com/images.wpr.com/flags/24/CZ.png"/></td><td><a href="/countries/czech-republic-population/">Czech Republic</a></td><td>78,865 km²</td><td>10,630,589</td><td>0.05%</td></tr><tr><td><img src="https://s3.amazonaws.com/images.wpr.com/flags/24/PT.png"/></td><td><a href="/countries/portugal-population/">Portugal</a></td><td>92,090 km²</td><td>10,254,666</td><td>-0.35%</td></tr><tr><td><img src="https://s3.amazonaws.com/images.wpr.com/flags/24/SE.png"/></td><td><a href="/countries/sweden-population/">Sweden</a></td><td>450,295 km²</td><td>10,053,135</td><td>0.71%</td></tr><tr><td><img src="https://s3.amazonaws.com/images.wpr.com/flags/24/AT.png"/></td><td><a href="/countries/austria-population/">Austria</a></td><td>83,871 km²</td><td>8,766,201</td><td>0.16%</td></tr><tr><td><img src="https://s3.amazonaws.com/images.wpr.com/flags/24/CH.png"/></td><td><a href="/countries/switzerland-population/">Switzerland</a></td><td>41,284 km²</td><td>8,608,259</td><td>0.75%</td></tr><tr><td><img src="https://s3.amazonaws.com/images.wpr.com/flags/24/IL.png"/></td><td><a href="/countries/israel-population/">Israel</a></td><td>20,770 km²</td><td>8,583,916</td><td>1.55%</td></tr><tr><td><img src="https://s3.amazonaws.com/images.wpr.com/flags/24/SG.png"/></td><td><a href="/countries/singapore-population/">Singapore</a></td><td>710 km²</td><td>5,868,104</td><td>1.32%</td></tr><tr><td><img src="https://s3.amazonaws.com/images.wpr.com/flags/24/DK.png"/></td><td><a href="/countries/denmark-population/">Denmark</a></td><td>43,094 km²</td><td>5,775,224</td><td>0.36%</td></tr><tr><td><img src="https://s3.amazonaws.com/images.wpr.com/flags/24/FI.png"/></td><td><a href="/countries/finland-population/">Finland</a></td><td>338,424 km²</td><td>5,561,389</td><td>0.34%</td></tr><tr><td><img src="https://s3.amazonaws.com/images.wpr.com/flags/24/NO.png"/></td><td><a href="/countries/norway-population/">Norway</a></td><td>323,802 km²</td><td>5,400,916</td><td>0.89%</td></tr><tr><td><img src="https://s3.amazonaws.com/images.wpr.com/flags/24/IE.png"/></td><td><a href="/countries/ireland-population/">Ireland</a></td><td>70,273 km²</td><td>4,847,139</td><td>0.90%</td></tr><tr><td><img src="https://s3.amazonaws.com/images.wpr.com/flags/24/NZ.png"/></td><td><a href="/countries/new-zealand-population/">New Zealand</a></td><td>270,467 km²</td><td>4,792,409</td><td>0.90%</td></tr><tr><td><img src="https://s3.amazonaws.com/images.wpr.com/flags/24/SI.png"/></td><td><a href="/countries/slovenia-population/">Slovenia</a></td><td>20,273 km²</td><td>2,081,900</td><td>0.03%</td></tr><tr><td><img src="https://s3.amazonaws.com/images.wpr.com/flags/24/EE.png"/></td><td><a href="/countries/estonia-population/">Estonia</a></td><td>45,227 km²</td><td>1,303,798</td><td>-0.23%</td></tr><tr><td><img src="https://s3.amazonaws.com/images.wpr.com/flags/24/CY.png"/></td><td><a href="/countries/cyprus-population/">Cyprus</a></td><td>9,251 km²</td><td>1,198,427</td><td>0.79%</td></tr><tr><td><img src="https://s3.amazonaws.com/images.wpr.com/flags/24/LU.png"/></td><td><a href="/countries/luxembourg-population/">Luxembourg</a></td><td>2,586 km²</td><td>596,992</td><td>1.13%</td></tr><tr><td><img src="https://s3.amazonaws.com/images.wpr.com/flags/24/IS.png"/></td><td><a href="/countries/iceland-population/">Iceland</a></td><td>103,000 km²</td>'


result = re.findall(r'href="\/countries.*?population\/">(\w.*?)<\/', html)

with open('firstWorldCountries.txt', 'w') as f:
	for item in result:
		f.write('%s\n' % item)