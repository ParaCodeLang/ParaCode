package main

// go build -o PCPM -ldflags "-s -w" main.go ; chmod +x PCPM

import (
  "fmt"
  "os"
  "net/http"
  "io/ioutil"
  "encoding/json"
  "strings"
  "strconv"
  "bytes"
  "path/filepath"
)

func later_version(a string, b string) string {
  sa := strings.Split(a, ".")
  sb := strings.Split(b, ".")
  for i := range sa {
    ia, _ := strconv.Atoi(sa[i])
    ib, _ := strconv.Atoi(sb[i])
    if (ia > ib) { return a }
    if (ib > ia) { return b }
  }
  
  return a
}

func main() {
  os.Mkdir("./pkg_data", 0755)

  if len(os.Args) < 2 {
    fmt.Println("PCPM expects at least one argument!")
    os.Exit(1)
  }

  if os.Args[1] != "install" && os.Args[1] != "get" && os.Args[1] != "update" && os.Args[1] != "remove" && os.Args[1] != "uninstall" && os.Args[1] != "publish" && os.Args[1] != "list" {
    fmt.Println("Invalid option " + os.Args[1] + "!")
    os.Exit(1)
  }

  if os.Args[1] == "publish" {
    if len(os.Args) != 4 {
      fmt.Println("Invalid number of arguments for command 'publish'!")
      os.Exit(1)
    }
  } else if os.Args[1] == "list" {
      files, _ := ioutil.ReadDir("./pkg_data/")
      any := false
      for i, f := range files {
        if f.IsDir() {
          any = true
          fmt.Println("Package " + fmt.Sprint(i + 1) + ": " + f.Name())
        }
      }
      if !any {
        fmt.Println("No packages are installed!")
        os.Exit(1)
      }
      os.Exit(0)
  } else {
    if len(os.Args) != 3 {
      fmt.Println("Invalid number of arguments for command '" + os.Args[1] + "'!")
      os.Exit(1)
    }
  }

  packagename := os.Args[2]

  if os.Args[1] == "publish" {
    jsonmap := map[string]string {
      "version": os.Args[3],
    }

    filepath.Walk("./" + packagename, func(path string, info os.FileInfo, err error) error {
      if !info.IsDir() {
        path = strings.Replace(path, packagename + "/", "", 1)

        dat, _ := ioutil.ReadFile("./" + packagename + "/" + path)
        jsonmap["_" + path] = string(dat)
      }
      return nil
    })
    
    // files, _ := ioutil.ReadDir("./" + packagename)
    
    // for _, f := range files {
    //   if f.IsDir() {
    //   } else {
    //     dat, _ := ioutil.ReadFile("./" + packagename + "/" + f.Name())
    //     jsonmap["_" + f.Name()] = string(dat)
    //   }
    // }

    requestBody, _ := json.Marshal(jsonmap)

    res, _ := http.Post("https://paracode-rewrite-cdn.darubyminer360.repl.co/publish/" + packagename, "application/json", bytes.NewBuffer(requestBody))

    respcode, _ := ioutil.ReadAll(res.Body);
    respstr := string(respcode)

    if respstr == "VERSION_EXISTS" {
      fmt.Println("That package version already exists!")
      os.Exit(1)
    }

    if respstr == "PACKAGE_EXISTS" {
      fmt.Println("That package already exists!")
      os.Exit(1)
    }

    fmt.Println("Package published.")

    defer res.Body.Close()
    os.Exit(0)
  }

  if _, err := os.Stat("./pkg_data/" + packagename); os.IsNotExist(err) {
    if os.Args[1] == "update" || os.Args[1] == "remove" || os.Args[1] == "uninstall" {
      fmt.Println("Package " + packagename + " is not installed!")
      os.Exit(1)
    }
  } else if os.Args[1] == "install" || os.Args[1] == "get" {
    fmt.Println("Package " + packagename + " is already installed!")
    os.Exit(1)
  }

  if os.Args[1] == "remove" || os.Args[1] == "uninstall" {
    os.RemoveAll("./pkg_data/" + packagename)
    os.Exit(0)
  }

  os.Mkdir("./pkg_data/" + packagename, 0755)

  resp, _ := http.Get("https://paracode-rewrite-cdn.darubyminer360.repl.co/package/" + packagename)
  if resp.StatusCode == 404 {
    fmt.Println("That package does not exist!")
    os.Remove("./pkg_data/" + packagename)
    os.Exit(1)
  }

  versions, _ := ioutil.ReadAll(resp.Body)
  var versions_arr []string;
  json.Unmarshal(versions, &versions_arr)

  latest := versions_arr[0]
  for i := range versions_arr {
    latest = later_version(latest, versions_arr[i])
  }

  resp, _ = http.Get("https://paracode-rewrite-cdn.darubyminer360.repl.co/package/" + packagename + "/" + latest)

  files, _ := ioutil.ReadAll(resp.Body)
  var files_arr []string;
  json.Unmarshal(files, &files_arr)

  for _, file := range files_arr {
    resp, _ = http.Get("https://paracode-rewrite-cdn.darubyminer360.repl.co/package/" + packagename + "/" + latest + "/" + file)

    contents, _ := ioutil.ReadAll(resp.Body)
    file, _ := os.Create("./pkg_data/" + packagename + "/" + file);
    file.Write(contents);
    defer file.Close();
  }
}
