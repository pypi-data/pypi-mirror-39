# flextable

tabular data formatter, for code, cli or pipes

## Purpose

Primarilary developed for ddb. It seemed prudent to seperate the concerns involved into different projects

### Pipe a file into a table

```bash
cat file | flextable  -d ',' -cc 9
```

### From the Terminal or Script

- This will load a text file 
- that has a ',' delimiter 
- starting at line 1
- for 10 lines
- with a column count of 9
- from a file named MOCK_DATA.csv

```bash
flextable  -d , --line 1 --length 10 -cc 9 --file  MOCK_DATA.csv
```

### format with code

```python
import flextable


 config = flextable.table_config()
 config.columns = ['column1','column2','column3','column4','column5','column6']
 results=[some python object with an array of arrays]
 flextable.table(data=results, args=config)
```

### Configuration

- flextanble accepts switches and environment variables
- switches take precidence

### Options

|Short|Long            |Default| Description                                                |
|----|-----------------|-------|------------------------------------------------------------|
|    |--file           |       | The input file to read                                     |
|-c  |--columns        |       | column names, comma seperated                              |
|-cc |--column-count   |       | column count, auto names columns 1-n                       |
|-hol|--header-on-line |       | auto populate column count/names from this row             |
|-rq |--remove-quote   |True   | unwrap fields with block quotes                            |
|-bq |--block-quote    |       | field block quote identifier                               |
|-ds |--data-on-line   |1      | data starts on this line                                   |
|-bs |--border-style   |SINGLE | change table style, SINGLE, DOUBBLE, ASCII                 |
|-nft|--no-footer      |True   | dont show the footer                                       |
|-nhd|--no-header      |True   | dont show header                                           |
|-ftc|--footer-columns |True   | footer has column names                                    |
|-hde|--header-every   |       | show header every (n) rows                                 |
|-e  |--error          |True   | rows with invalid number of columns are considered errors  |
|-cm |--comment        |'#'    | character that denotes line is comment                     |
|-d  |--delimiter      |','    | field delimiter                                            |
|-he |--hide-errors    |False  | do not display errors                                      |
|-hc |--hide-comments  |False  | do not display comments                                    |
|-hw |--hide-whitespace|False  | do not display whitespace                                  |
|-l  |--line           |1      | line number to start displaying data                       |
|-len|--length         |       | number of lines to show, hidden elements count             |
|-p  |--page           |       | page to start displaying, requires length parameter        |
|-ow |--width          | auto  | width of output in characters, if not specified calculated |
|-oh |--height         |       | height of output window in characters                      |
|-nc |--no-color       |False  | disale color output                                        |
|-o  |--output         |ASCII  | ASCII, YAML, JSON                                          |


## Environment vars

|Long             |Environment Var   |
|-----------------|------------------|
|--file           |FT_FILE           |
|--columns        |FT_COLUMNS        |
|--column-count   |FT_COLUMN_COUNT   |
|--header-on-line |FT_HEADER_ON_LINE |
|--remove-quote   |FT_REMOVE_QUOTE   |
|--block-quote    |FT_BLOCK_QUOTE    |
|--data-on-line   |FT_DATA_ON_LINE   |
|--border-style   |FT_BORDER_STYLE   |
|--no-footer      |FT_NO_FOOTER      |
|--no-header      |FT_NO_HEADER      |
|--footer-columns |FT_FOOTER_COLUMNS |
|--header-every   |FT_HEADER_EVERY   |
|--error          |FT_ERROR          |
|--comment        |FT_COMMENT        |
|--delimiter      |FT_DELIMITER      |
|--hide-errors    |FT_HIDE_ERRORS    |
|--hide-comments  |FT_HIDE_COMMENTS  |
|--hide-whitespace|FT_HIDE_WHITESPACE|
|--line           |FT_LINE           |
|--length         |FT_LENGTH         |
|--page           |FT_PAGE           |
|--width          |FT_WIDTH          |
|--height         |FT_HEIGHT         |
|--no-color       |FT_NO_COLOR       |
|--output         |FT_OUTPUT         |

### CLI Results

```text
 #flextable MOCK_DATA.csv -l 1 -len 10 -cc 6 -d ,  
┌┤column1    ├┬┤column2    ├┬┤column3    ├┬┤column4    ├┬┤column5    ├┬┤column6    ├┐
│id           │first_name   │last_name    │email        │gender       │ip_address   │
│2            │Redford      │Ornils       │rornils1@amaz│Male         │24.42.186.82 │
│3            │Grenville    │Buckley      │gbuckley2@giz│Male         │143.223.126.2│
│4            │Thalia       │Badrock      │tbadrock3@xin│Female       │113.57.179.78│
│5            │Julie        │Minchell     │jminchell4@sk│Female       │105.165.149.1│
│6            │Lancelot     │Archibold    │larchibold5@p│Male         │213.155.189.4│
│7            │Bernie       │Matteucci    │bmatteucci6@b│Male         │109.156.49.36│
│8            │Flinn        │Mulchrone    │fmulchrone7@n│Male         │22.84.116.46 │
│9            │Seamus       │Tocque       │stocque8@cnet│Male         │79.30.35.75  │
│10           │Lazare       │Abbett       │labbett9@who.│Male         │17.173.76.145│
└[column1    ]┴[column2    ]┴[column3    ]┴[column4    ]┴[column5    ]┴[column6    ]┘

```

## JSON RESULTS

```json
#flextable MOCK_DATA.csv -l 1 -len 10 -cc 6 -d , -o json
{"header": ["column1", "column2", "column3", "column4", "column5", "column6"], "rows": [{"type": 3, "data": ["id", "first_name", "last_name", "email", "gender", "ip_address"], "file_line_number": 1, "error": null}, {"type": 3, "data": ["2", "Redford", "Ornils", "rornils1@amazon.co.uk", "Male", "24.42.186.82"], "file_line_number": 2, "error": null}, {"type": 3, "data": ["3", "Grenville", "Buckley", "gbuckley2@gizmodo.com", "Male", "143.223.126.204"], "file_line_number": 3, "error": null}, {"type": 3, "data": ["4", "Thalia", "Badrock", "tbadrock3@xinhuanet.com", "Female", "113.57.179.78"], "file_line_number": 4, "error": null}, {"type": 3, "data": ["5", "Julie", "Minchell", "jminchell4@skyrock.com", "Female", "105.165.149.121"], "file_line_number": 5, "error": null}, {"type": 3, "data": ["6", "Lancelot", "Archibold", "larchibold5@pinterest.com", "Male", "213.155.189.44"], "file_line_number": 6, "error": null}, {"type": 3, "data": ["7", "Bernie", "Matteucci", "bmatteucci6@bravesites.com", "Male", "109.156.49.36"], "file_line_number": 7, "error": null}, {"type": 3, "data": ["8", "Flinn", "Mulchrone", "fmulchrone7@naver.com", "Male", "22.84.116.46"], "file_line_number": 8, "error": null}, {"type": 3, "data": ["9", "Seamus", "Tocque", "stocque8@cnet.com", "Male", "79.30.35.75"], "file_line_number": 9, "error": null}, {"type": 3, "data": ["10", "Lazare", "Abbett", "labbett9@who.int", "Male", "17.173.76.145"], "file_line_number": 10, "error": null}]}

```

### YAML RESULTS

```yaml
#flextable MOCK_DATA.csv -l 1 -len 10 -cc 6 -d , -o yaml
header: [column1, column2, column3, column4, column5, column6]
rows:
- data: [id, first_name, last_name, email, gender, ip_address]
  error: null
  file_line_number: 1
  type: 3
- data: ['2', Redford, Ornils, rornils1@amazon.co.uk, Male, 24.42.186.82]
  error: null
  file_line_number: 2
  type: 3
- data: ['3', Grenville, Buckley, gbuckley2@gizmodo.com, Male, 143.223.126.204]
  error: null
  file_line_number: 3
  type: 3
- data: ['4', Thalia, Badrock, tbadrock3@xinhuanet.com, Female, 113.57.179.78]
  error: null
  file_line_number: 4
  type: 3
- data: ['5', Julie, Minchell, jminchell4@skyrock.com, Female, 105.165.149.121]
  error: null
  file_line_number: 5
  type: 3
- data: ['6', Lancelot, Archibold, larchibold5@pinterest.com, Male, 213.155.189.44]
  error: null
  file_line_number: 6
  type: 3
- data: ['7', Bernie, Matteucci, bmatteucci6@bravesites.com, Male, 109.156.49.36]
  error: null
  file_line_number: 7
  type: 3
- data: ['8', Flinn, Mulchrone, fmulchrone7@naver.com, Male, 22.84.116.46]
  error: null
  file_line_number: 8
  type: 3
- data: ['9', Seamus, Tocque, stocque8@cnet.com, Male, 79.30.35.75]
  error: null
  file_line_number: 9
  type: 3
- data: ['10', Lazare, Abbett, labbett9@who.int, Male, 17.173.76.145]
  error: null
  file_line_number: 10
  type: 3
```