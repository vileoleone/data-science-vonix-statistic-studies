const fs = require('fs')
const { faker } = require('@faker-js/faker')
fs.open('tests/src/lib/fixtures/dummy-data.csv', 'w+', function (err, file) {
  if (err) throw err

  for (let i = 0; i < 1000; i++) {
    const number = faker.datatype.number({ min: 1, max: 5400 })

    // fs.writeSync(file, number)
    // number = faker.phone.number('02#3#######\n')

    // fs.writeSync(file, number)
    // number = faker.phone.number('3#3#######\n')

    // fs.writeSync(file, number)
    // number = faker.phone.number('05#9########\n')

    fs.writeSync(file, String(number))
    fs.writeSync(file, '\n')
  }
  fs.close(file)
})
