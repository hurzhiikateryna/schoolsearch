# Schoolsearch

Консольна програма для роботи з даними про учнів школи.

## Що вміє

- шукати учня за прізвищем;
- шукати учнів за вчителем;
- шукати за класом або автобусом;
- оновлювати дані учня;
- видаляти учня;
- вимірювати час пошуку.

## Формат даних

Файл `students.txt` містить рядки такого вигляду:

```text
LASTNAME,FIRSTNAME,GRADE,CLASSROOM,BUS,TEACHER_LASTNAME,TEACHER_FIRSTNAME
```

Наприклад:

```text
COOKUS,XUAN,3,107,52,FAFARD,ROCIO
```

## Запуск

```bash
python schoolsearch.py
```

## Команди

```text
S: COOKUS
S: COOKUS B
T: FAFARD
C: 107
B: 52
D: LASTNAME,FIRSTNAME
U: LASTNAME,FIRSTNAME
Q
```

## Примітка

Програма читає дані з `students.txt` і зберігає зміни назад у цей файл.
