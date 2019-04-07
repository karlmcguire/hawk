package main

import (
	"encoding/csv"
	"encoding/json"
	"os"
)

type Listings struct {
	Data []*Data `json:"data"`
}

type Data struct {
	Id          int    `json:"id"`
	Name        string `json:"name"`
	Symbol      string `json:"symbol"`
	WebsiteSlug string `json:"website_slug"`
}

func main() {
	var (
		listings = &Listings{}
		dec      = json.NewDecoder(os.Stdin)
	)

	if err := dec.Decode(&listings); err != nil {
		panic(err)
	}

	out := make([][]string, len(listings.Data))

	for i, l := range listings.Data {
		out[i] = make([]string, 3)

		out[i][0] = l.Symbol
		out[i][1] = l.WebsiteSlug
		out[i][2] = l.Name
	}

	w := csv.NewWriter(os.Stdout)
	for _, r := range out {
		if err := w.Write(r); err != nil {
			panic(err)
		}
	}

	w.Flush()

	if err := w.Error(); err != nil {
		panic(err)
	}
}
