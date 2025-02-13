package pkgecosystem_test

import (
	"bytes"
	"testing"

	"github.com/ossf/package-analysis/pkg/api/pkgecosystem"
	"golang.org/x/exp/slices"
)

func TestEcosystemMarshalText(t *testing.T) {
	tests := []struct {
		name string
		eco  pkgecosystem.Ecosystem
		want []byte
	}{
		{
			name: "wolfi",
			eco:  pkgecosystem.Wolfi,
			want: []byte("wolfi"),
		},
		{
			name: "unsupported",
			eco:  pkgecosystem.Ecosystem("this is a test"),
			want: []byte("this is a test"),
		},
		{
			name: "empty",
			eco:  pkgecosystem.None,
			want: []byte{},
		},
	}
	for _, test := range tests {
		t.Run(test.name, func(t *testing.T) {
			got, _ := test.eco.MarshalText()
			if !bytes.Equal(got, test.want) {
				t.Errorf("MarshalText() = %v; want %v", got, test.want)
			}
		})
	}
}

func TestEcosystemUnmarshalText(t *testing.T) {
	tests := []struct {
		name    string
		input   []byte
		want    pkgecosystem.Ecosystem
		wantErr bool
	}{
		{
			name:  "wolfi",
			input: []byte("wolfi"),
			want:  pkgecosystem.Wolfi,
		},
		{
			name:    "unsupported",
			input:   []byte("this is a test"),
			wantErr: true,
		},
		{
			name:  "empty",
			input: []byte{},
			want:  pkgecosystem.None,
		},
	}
	for _, test := range tests {
		t.Run(test.name, func(t *testing.T) {
			var got pkgecosystem.Ecosystem
			err := got.UnmarshalText(test.input)
			if test.wantErr && err == nil {
				t.Fatal("UnmarshalText() is nil; want error")
			}
			if !test.wantErr && err != nil {
				t.Fatalf("UnmarshalText() = %v; want nil", err)
			}
			if got != test.want {
				t.Errorf("UnmarshalText() parsed %v; want %v", got, test.want)
			}
		})
	}
}

func TestEcosystemString(t *testing.T) {
	tests := []struct {
		name string
		eco  pkgecosystem.Ecosystem
		want string
	}{
		{
			name: "wolfi",
			eco:  pkgecosystem.Wolfi,
			want: "npm",
		},
		{
			name: "unsupported",
			eco:  pkgecosystem.Ecosystem("this is a test"),
			want: "this is a test",
		},
		{
			name: "empty",
			eco:  pkgecosystem.Ecosystem(""),
			want: "",
		},
	}
	for _, test := range tests {
		t.Run(test.name, func(t *testing.T) {
			got := test.eco.String()
			if got != test.want {
				t.Errorf("String() = %v; want %v", got, test.want)
			}
		})
	}
}

func TestEcosystemsAsStrings(t *testing.T) {
	want := []string{"npm", "pypi", "rubygems"}
	got := pkgecosystem.EcosystemsAsStrings([]pkgecosystem.Ecosystem{
		pkgecosystem.Wolfi,
	})
	if !slices.Equal(got, want) {
		t.Errorf("EcosystemsAsStrings() = %v; want %v", got, want)
	}
}
