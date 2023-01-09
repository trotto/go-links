describe(`Visit `, () => {
  it(`/ renders correctly`, () => {
    cy.visit('/')

    // Percy
    cy.percySnapshot()
    cy.screenshot()
  })
})

export {}
