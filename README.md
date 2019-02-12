# software-design
## hw01
[![Build Status](https://travis-ci.org/Igor-Tukh/software-design.svg?branch=hw01-CLI)](https://travis-ci.org/Igor-Tukh/software-design)

Запуск:
```
<change directory to source in hw01-CLI>
python3 cli.py
```

В данной домашней работе можно выделить несколько модулей:
* Первый из них, это CLI, модуль, который обрабатывает пользовательский ввод, последовательно обращаясь к другим модулям и запрашивая результат их работы. После выполняет полученные команды. При этом в данной реализации он не отделен от ввода/вывода, т.к. некоторая логика (вывести '>>>' или '>' и т.д.) напрямую зависит от работы логического куска этого модуля. Разделение возможно, но мне кажется в данной ситуации не вполне оправданым ввиду простоты краткости модуля. Тем не менее, это делается достаточно легко, если что.
* Tokenizer, модуль, которому последовательно подеются на вход ползовательский ввод. После чего у него можно запросить токены. Он хранит промежуточную информацию (например, если была подана строка, оканчивающаяся на кавычку, возможно, некоторый из токенов еще не закончен). Токены будут возвращены только если последний токен завершился. Также в этом модуле производется подстановка для токенов вида $a (формально, эту часть также можно было выделить в отдельный модуль, но т.к. обработка этих строк происходит "в онлайне", в процессе построения токенов, а в отдельном модуле потребовала бы дополнительного прохода по уже обработанным токенам, это кажется возможным допущением).
* Interpreter, модуль, который формирует команды из токенов. Он также хранит промежуточную информацию (например, если строка оканчивается на | (пайп), то необоходимо подождать, пока будут введены оставшиеся команды). У него можно запросить построенные команды, если последний токен не является пайпом. Знает про доступные реализации команд.
* Commands, модуль, состоит из классов-реализаций различных команд. Для добавления новой команды необходимо описать подобный класс и сообщить об этом интерпретеру.

![alt text](https://github.com/Igor-Tukh/software-design/blob/hw01-CLI/hw01-CLI/hw01.png)

## hw02

Выбор библиотеки для разбора аргументов.

Для разбора аргументов в питоне, как правило, используют одну из предыдущих библиотек:

  * **getopt** -- модуль, являющийся C-style парсером для аргументов командной строки (стандартная библиотека). Использовался в старых версиях питона. Доступен и в новых, но согласно замечанию из документации, для пользователей, которые не знакомы с функцией из C getopt(), а так же для тех, кто хочет писать меньше кода или лучше обрабатывать ошибки, предпочтительней использовать *argparse*.
  * **optparse** -- библиотека из стандартной библиотеки. Согласно документации более мощная, гибкая и удобная, чем старый модуль getopt. Использует декларативный стиль разбора командной строки. Тем не менее *deprecated since version 2.7 and will not be developed further*, мы же используем python3. Разработка продолжилась в модуле *argparse*
  * **argparse** -- стандартная библиотека, которая позволяет "легко реализовать user-friendly command-line interfaces". Автоматически генерирует help, а также умеет обрабатывать ошибки и некорректные аргументы. Согласно моему личному опыту, наиболее часто используется именно она (в тех проектах, с которыми я сталкивался), проста и приятна в использовании.
  * **plac** -- Сторонняя библиотека. Функциональность уже, чем у argparse (согласно документации!), утверждается, менее многословная, чем последняя.
  * **docopt** -- сторонняя библиотека. Согласно документации:
  
    docopt helps you:
    * define the interface for your command-line app, and
    * automatically generate a parser for it.
  
  Это звучит достаточно круто. 

Тем не менее я остановился на argparse по следующим причинам:
    
  * У меня есть опыт работы с данной библиотекой
  * Я считаю ее достаточно удобной
  * docopt доступна для многих языков программирования, а arparse является стандартной питоновской библиотекой, что говорит о том, что в ней, вероятно, особенности питона будут учтены лучше (хотя какие там особенности?)
  * А также, в том или инном виде argparse будет развиваться вместе с питоном. Судьба же docopt неясна.
  * Первые два варианта использовать не целесообразно  по причинам, обозначенным при их описании.
  * Не plac ввиду того, что ИМХО парсер в рамках данной задачи (для grep) все равно будет достаточно лакончиным и в argparse. А других достоинств не увидел.
  