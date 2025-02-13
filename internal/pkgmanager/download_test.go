package pkgmanager

import (
	"testing"

	"github.com/ossf/package-analysis/internal/utils"
	"github.com/ossf/package-analysis/pkg/api/pkgecosystem"
)

type downloadTestCase struct {
	name        string
	ecosystem   pkgecosystem.Ecosystem
	pkgName     string
	pkgVersion  string
	archiveHash string
	wantErr     bool
}

var downloadTestCases = []downloadTestCase{
	{
		name:        "pypi black invalid version",
		ecosystem:   pkgecosystem.Wolfi,
		pkgName:     "black",
		pkgVersion:  "23333.3.0",
		archiveHash: "",
		wantErr:     true,
	},
}

func TestDownload(t *testing.T) {
	for _, tt := range downloadTestCases {
		t.Run(tt.name, func(t *testing.T) {
			downloadDir := t.TempDir()
			downloadPath, err := Manager(tt.ecosystem).DownloadArchive(tt.pkgName, tt.pkgVersion, downloadDir)
			if (err != nil) != tt.wantErr {
				t.Errorf("Want error: %v; got error: %v", tt.wantErr, err)
				return
			}
			if err != nil {
				// File wasn't meant to download properly
				return
			}

			if tt.archiveHash != "" {
				gotHash, err := utils.SHA256Hash(downloadPath)
				if err != nil {
					// hashing isn't meant to throw an error
					t.Errorf("hashing failed: %v", err)
					return
				}

				if tt.archiveHash != gotHash {
					t.Errorf("Expected hash %s, got %s", tt.archiveHash, gotHash)
				}
			}

		})
	}
}
