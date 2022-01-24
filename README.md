![logo](static/images/pakuri3-banner.png)
![Mark](https://img.shields.io/badge/PAKURI-Mark%20III-red)
![License](https://img.shields.io/github/license/01rabbit/PAKURI)
![release-date](https://img.shields.io/github/release-date/01rabbit/PAKURI-THON)
![sns](https://img.shields.io/twitter/follow/PAKURI9?label=PAKURI&style=social)

# PAKURI-THON

Pentest Achieve Knowledge Unite Rapid Interface - Python  
PAKURI-THON is a tool that supports pentesters with various pentesting tools and C4 server (command & control and chat & communication server). PAKURI-THON can perform most of the operations with intuitive web operations and commands to chatbots.

## What is PAKURI

I've consulted many pentesting tools. I then took the good points of those tools and incorporated them into my own tools. In Japanese slang, imitation is also called "paku-ru".
> ぱくる (godan conjugation, hiragana and katakana パクる, rōmaji pakuru)
>
> 1. eat with a wide open mouth
> 2. steal when one isn't looking, snatch, swipe  
> 3. copy someone's idea or design  
> 4. nab, be caught by the police  
>
> [Wiktionary:ぱくる](https://en.wiktionary.org/wiki/%E3%81%B1%E3%81%8F%E3%82%8B "ぱくる")

## Why Develop this Tool?

PAKURI-THON is an upgraded version of PAKURI that was presented at the 2020 Blackhat Asia Arsenal.
After the COVID-19 pandemic, the way we work has changed drastically and working remotely from home instead of going to the office has become the norm. This change in the way we work has increased security risks, raised awareness of security and increased the demand for pen testing.  
However, there is still a shortage of security personnel in Japan. As the workload increases while the manpower does not, pen-testing becomes a monotonous and boring job, lowering the quality.  
So, if we automate the boring and simple work, the machine will do the same work over and over again with accuracy, but is that really enough? Pen testing tools are also becoming more and more automated, but is that really enough?  
I don't think so. I don't want to let machines take all the fun out of my life. But I don't like boring work. So I decided to enjoy boring work together with machines. The answer is PAKURI-THON.  
PAKURI-THON was rebuilt in Python to improve the usability of PAKURI. As a result, it implements a web interface, making it much more intuitive and stylish than before.
Specifically, once PAKURI-THON is connected to the target network, it can be operated from a smartphone or tablet.  
You can also use chat to share information with your team. Also, most operations can be solved by giving instructions to the bot. Therefore, there is no need to switch the method of information sharing when working with a team.
Best of all, wouldn't it be cool to be able to do a pen test just by talking to the machine using your smartphone, just like the hacker in the movie?

---

## Features

- The web interface is implemented so that it can be operated intuitively on smartphones and tablets. We were able to fit all of the pentests into the palm of our hand.
- Since we have a terminal in the web interface, you can operate the Kali Linux terminal directly from your smartphone or tablet. If you are using a tablet, you can hold it horizontally to enable some keyboard operations.
- The use of chatbots. Just talk to the chatbot (give instructions) and it will execute the command, which increases convenience as there is no need to switch the means of information sharing within the team.
- PowerShell Empire, which is used in actual cyber attacks, can be controlled through a web interface and can easily be used for red team training.

## Tool used

### Reconnaissance

- [Nmap](https://www.kali.org/tools/nmap/)
- [Nikto](https://www.kali.org/tools/nikto/)
- [AutoRecon](https://github.com/Tib3rius/AutoRecon)

### Post Exploit

- [PowerShell Empire](https://www.kali.org/tools/powershell-empire/)

### Misc

- [WebSSH](https://github.com/huashengdun/webssh)
- [Nextcloud](https://github.com/nextcloud)

|**NOTE**  |
|:----------------|
|If you are interested, please use them in an environment **under your control and at your own risk**. And, if you execute the PAKURI-THON on systems that are not under your control, it may be considered an attack and you may have legally liabillity for your action.|


## Install

Check out the [PAKURI-THON wiki](https://github.com/01rabbit/PAKURI-THON/wiki) for instructions on getting started with PAKUTI-THON.

## Screenshot

### Main menu

![main](https://user-images.githubusercontent.com/16553787/150373461-54ccf9bd-282e-477f-a7d9-718427029032.png)

### Target

![target](https://user-images.githubusercontent.com/16553787/150374348-78541bb6-e567-40e9-8e09-f696dce558d6.png)

![host](https://user-images.githubusercontent.com/16553787/150375012-b956b589-b504-4a83-84d5-a125d5f80955.png)

### Recon

![recon1](https://user-images.githubusercontent.com/16553787/150374615-a8a29669-98c5-42ea-abe2-c99f7000f859.png)

![recon2](https://user-images.githubusercontent.com/16553787/150374846-c6b36c14-6034-4f1f-bfdd-35721da738c4.png)

![port](https://user-images.githubusercontent.com/16553787/150375148-029fcffc-f7e7-4318-a411-39b6c5bbd4be.png)

### Post-Exsploit

![tool](https://user-images.githubusercontent.com/16553787/150375389-7097db57-f46e-425d-929b-08eb2ab390f6.png)

### Terminal

![terminal](https://user-images.githubusercontent.com/16553787/150375599-dc4f1708-5628-4a41-a9e2-d5800ce814b8.png)

### Chat : Nextcloud

![chat](https://user-images.githubusercontent.com/16553787/150375922-858e1764-f90a-4329-a047-1c187e4cf1b6.png)

### Docker

![docker](https://user-images.githubusercontent.com/16553787/150376075-61a5c06e-dff3-401d-95cf-0b8aa3a15fb1.png)

### Smartphone

![IMG_1166](https://user-images.githubusercontent.com/16553787/150376495-5cc58397-e9f6-42c3-aa0e-a52e1302a3ab.PNG)

![IMG_1167](https://user-images.githubusercontent.com/16553787/150376486-99222b26-2b5c-426a-95e9-9ab4a298b0d3.PNG)

![IMG_1168](https://user-images.githubusercontent.com/16553787/150376461-ccfc3b50-f833-4f02-9313-d3346c3c1a0c.PNG)

---

PAKURI is not fully automated and requires the user interactions, to make sure to proceed the pentest and to avoid any unintended attack or trouble.  

---

## Operation check environment

- OS: KAli Linux 2021.4a
- Memory: 8.0GB
- Browser:
  - Firefox: 96.0
  - Google Chrome: 97.0
  - Chromium: 97.0
  - Brave: 1.34.81

## Known Issues

- This is intended for use Kali Linux. Operation on other OS is not guaranteed.

---

## Contributors

If you have some new idea about this project, issue, feedback or found some valuable tool feel free to open an issue for just DM me via [@Mr.Rabbit](https://twitter.com/01ra66it) or [@PAKURI](https://twitter.com/PAKURI9).
