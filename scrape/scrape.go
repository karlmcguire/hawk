package main

import (
	"bytes"
	"encoding/csv"
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
	"strings"
	"time"
)

const (
	URL_PRE = "https://coinmarketcap.com/currencies/"
	URL_SUF = "/historical-data/?start=20171020&end=20181020"
	CHROME  = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"
)

func main() {
	dec := csv.NewReader(os.Stdin)
	cur, err := dec.ReadAll()
	if err != nil {
		panic(err)
	}

	// create the http client
	c := &http.Client{}

	for z := 2104; z < len(cur); z++ {
		// create the http request
		// TODO: commandline argument for currency name and time period (URL_SUF)
		req, err := http.NewRequest("GET", URL_PRE+cur[z][1]+URL_SUF, nil)
		if err != nil {
			panic(err)
		}
		req.Header.Set("User-Agent", CHROME)

		// send the request
		res, err := c.Do(req)
		if err != nil {
			panic(err)
		}
		defer res.Body.Close()

		// convert res.Body to []byte
		dat, err := ioutil.ReadAll(res.Body)
		if err != nil {
			panic(err)
		}

		// get the table only
		var (
			start = bytes.Index(dat, []byte("<tbody>"))
			end   = bytes.Index(dat, []byte("</tbody>")) + 8
			table = dat[start:end]
			lines = bytes.Split(table, []byte("\n"))
			count = bytes.Count(table, []byte("<tr"))
			data  = make([][]byte, count*7)
			days  = make([][]string, count)
			raw   = make([]string, 7)
		)

		n := 0
		for i := 0; i < len(lines); i++ {
			if bytes.Contains(lines[i], []byte("data-format")) || bytes.Contains(lines[i], []byte("text-left")) {
				data[n] = lines[i]
				n++
			}
		}

		for i := 0; i < len(data); i += 7 {
			for a := 0; a < 7; a++ {
				var (
					l = data[i+a]
					s = bytes.Index(l, []byte(">")) + 1
					e = bytes.Index(l, []byte("</"))
				)

				raw[a] = string(l[s:e])
			}

			n := i / 7

			days[n] = make([]string, 7)

			// convert from string to time
			t, err := time.Parse("Jan 02, 2006", raw[0])
			if err != nil {
				panic(err)
			}

			days[n][0] = t.Format(time.RFC822)
			days[n][1] = raw[1]
			days[n][2] = raw[2]
			days[n][3] = raw[3]
			days[n][4] = raw[4]
			days[n][5] = strings.Replace(raw[5], ",", "", -1)
			days[n][6] = strings.Replace(raw[6], ",", "", -1)
		}

		f, err := os.Create(cur[z][0] + ".csv")
		if err != nil {
			panic(err)
		}

		// write the output as csv
		w := csv.NewWriter(f)
		for _, d := range days {
			if err = w.Write(d); err != nil {
				panic(err)
			}
		}
		w.Flush()
		if err = w.Error(); err != nil {
			panic(err)
		}

		f.Close()

		fmt.Printf("[%d/%d] %s\n", z, len(cur), cur[z][0])
	}
}
