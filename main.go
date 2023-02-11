/*
Copyright © 2021 NAME HERE <EMAIL ADDRESS>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/
package main

import (
	"fmt"
	"os"
	"os/signal"
	"syscall"

	"github.com/github.com/TheAwesomeProgrammer/autorestic/autorestic/cmd"
	"github.com/github.com/TheAwesomeProgrammer/autorestic/autorestic/internal/lock"
)

func handleCtrlC() {
	c := make(chan os.Signal)
	signal.Notify(c, os.Interrupt, syscall.SIGTERM)
	go func() {
		sig := <-c
		fmt.Println("Signal:", sig)
		lock.Unlock()
		os.Exit(0)
	}()
}

func main() {
	handleCtrlC()
	cmd.Execute()
}
