package main

import (
	"fmt"
	"bufio"
	"strings"
	"os"
	"os/exec"

	"atomicgo.dev/keyboard"
	"atomicgo.dev/keyboard/keys"
	"github.com/pterm/pterm"
	"github.com/google/shlex"
)

func CheckExec() string {
	bin, err := exec.LookPath("ewfts")
	if err != nil {
		fmt.Println("Required Tool 'ewfts' Not Found, Please install it into your system PATH")
		os.Exit(1)
	}
	return bin
}

func PickedExec() {
	bin := CheckExec()
	scanner := bufio.NewScanner(os.Stdin)
	fmt.Println("Enter Arguments: ")
	var argsu string
	if scanner.Scan() {
		argsu = scanner.Text()
	}
	args, err := shlex.Split(argsu)
	if err != nil {
		fmt.Printf("Invalid args: %v\n", err)
		return
	}
	cmd := exec.Command(bin, args...)
	cmd.Stdin = os.Stdin
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr
	if err := cmd.Run(); err != nil {
		fmt.Printf("CLI error: %v\n", err)
	}
}

func main() {
	CheckExec()
	options := []string{"Exec", "Exit"}
	selected := 0

	render := func() {
		var lines []string
		for i, opt := range options {
			if i == selected {
				lines = append(lines, pterm.Green(fmt.Sprintf("    %-18s", opt)))
			} else {
				lines = append(lines, fmt.Sprintf("   %-18s", opt))
			}
		}

		box := pterm.DefaultBox.
			WithTitle(pterm.Gray(" Main Menu ")).
			WithTitleTopCenter().
			Sprint(strings.Join(lines, "\n"))

		cat := pterm.Cyan(`
        EWFTS TUI
                __ _
  _____      __/ _| |_ ___
 / _ \ \ /\ / / |_| __/ __|
|  __/\ V  V /|  _| |_\__ \
 \___| \_/\_/ |_|  \__|___/


				`)
		screen := strings.ReplaceAll(cat+"\n"+box, "\n", "\r\n")

		fmt.Print("\033[H\033[2J" + screen + "\r\n")
	}

	render()

	keyboard.Listen(func(key keys.Key) (bool, error) {
		switch key.Code {
		case keys.Up:
			selected = (selected - 1 + len(options)) % len(options)
			render()
		case keys.Down:
			selected = (selected + 1) % len(options)
			render()
		case keys.Enter:
			return true, nil
		case keys.CtrlC:
			selected = len(options) - 1
			return true, nil
		}
		return false, nil
	})

	switch options[selected] {
	case "Exec":
		PickedExec()
	case "Exit":
		fmt.Println("Exiting...")
	default:
		fmt.Println("???")
	}
}
