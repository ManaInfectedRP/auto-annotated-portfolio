---
type: PageLayout
title: About
colors: colors-a
backgroundImage:
  type: BackgroundImage
  url: /images/bg4.jpg
  backgroundSize: cover
  backgroundPosition: center
  backgroundRepeat: no-repeat
  opacity: 75
sections:
  - elementId: ''
    colors: colors-f
    backgroundSize: full
    text: >+
      # Hey, I'm Sebastian Larsson! I'm a passionate software developer currently studying AI development at NBI/Handelsakademin in Halmstad, Sweden.
      
      I have a unique background combining automotive industry experience with modern software development. My journey started in the automotive sector where I worked as a mechanic and in warehouse operations, giving me strong problem-solving skills and attention to detail.

      Now I'm focused on building my expertise in software development, particularly with C# and AI technologies. I'm actively seeking a LIA internship for 2026 where I can apply my skills and continue learning.
      
      When I'm not coding, you can find me exploring new technologies or working on personal projects. Check out my work on [GitHub](https://github.com/ManaInfectedRP)!

    media:
      type: ImageBlock
      url: /images/about.jpg
      altText: Hero image
    styles:
      self:
        height: auto
        width: wide
        margin:
          - mt-0
          - mb-0
          - ml-0
          - mr-0
        padding:
          - pt-16
          - pb-12
          - pl-4
          - pr-4
        textAlign: left
    type: HeroSection
  - type: DividerSection
    styles:
      self:
        width: wide
        padding:
          - pt-12
          - pb-12
          - pl-4
          - pr-4
        borderWidth: 1
        borderStyle: solid
  - type: LabelsSection
    colors: colors-f
    subtitle: 'Technical Skills:'
    items:
      - type: Label
        label: 'C#'
      - type: Label
        label: '.NET'
      - type: Label
        label: 'AI Development'
      - type: Label
        label: 'Software Development'
      - type: Label
        label: 'Microsoft Office'
      - type: Label
        label: 'Problem Solving'
      - type: Label
        label: 'Automotive Systems'
      - type: Label
        label: 'Warehouse Operations'
  - type: DividerSection
    styles:
      self:
        width: wide
        padding:
          - pt-12
          - pb-12
          - pl-4
          - pr-4
        borderWidth: 1
        borderStyle: solid
  - type: TextSection
    variant: variant-a
    subtitle: 'Contact:'
    colors: colors-f
    text: |
      [sebbelarsson9601@gmail.com](mailto:sebbelarsson9601@gmail.com)
      
      Phone: 0768-855568
      
      [LinkedIn](https://www.linkedin.com/in/sebastian-larsson-b45803246/)
      
      [GitHub](https://github.com/ManaInfectedRP)
  - type: DividerSection
    styles:
      self:
        width: wide
        padding:
          - pt-8
          - pb-8
          - pl-4
          - pr-4
        borderWidth: 1
        borderStyle: solid
  - type: FeaturedItemsSection
    colors: colors-f
    items:
      - type: FeaturedItem
        subtitle: 'Experience:'
        text: |-
          **Current Since (2024)**

          * Software Development Student with AI specialization @ NBI/Handelsakademin

          **2023**

          * Warehouse Worker & Picker @ Enyroom AB, Halmstad

          **2019-2020**

          * Mechanic @ Göstorps Nissan Bil AB, Laholm

          **2018**

          * Tire Picker @ Motor AB Halland Däckhotell, Halmstad
          * Warehouse Assistant @ Hedin Bil

          **2014-2015**

          * Mechanic Trainee @ YA Carlsson Snabbservice AB, Halmstad
        styles:
          self:
            textAlign: left
      - type: FeaturedItem
        subtitle: 'Education:'
        text: |-
          **Current (2024)**

          * Software Development with AI specialization @ NBI/Handelsakademin, Halmstad

          **2012-2015**

          * Vehicle & Transport Program (Truck specialization) @ Kattegattgymnasiet, Halmstad
        styles:
          self:
            textAlign: left
    columns: 2
    spacingX: 60
    spacingY: 60
    styles:
      self:
        height: auto
        width: wide
        padding:
          - pt-8
          - pb-8
          - pl-4
          - pr-4
        textAlign: left
  - type: DividerSection
    styles:
      self:
        width: wide
        padding:
          - pt-12
          - pb-12
          - pl-4
          - pr-4
        borderWidth: 1
        borderStyle: solid
  - type: ContactSection
    backgroundSize: full
    title: "Let's talk... 💬"
    colors: colors-f
    form:
      type: FormBlock
      elementId: sign-up-form
      fields:
        - name: firstName
          label: First Name
          hideLabel: true
          placeholder: First Name
          isRequired: true
          width: 1/2
          type: TextFormControl
        - name: lastName
          label: Last Name
          hideLabel: true
          placeholder: Last Name
          isRequired: false
          width: 1/2
          type: TextFormControl
        - name: email
          label: Email
          hideLabel: true
          placeholder: Email
          isRequired: true
          width: full
          type: EmailFormControl
        - name: message
          label: Message
          hideLabel: true
          placeholder: Tell me about your project
          isRequired: true
          width: full
          type: TextareaFormControl
        - name: updatesConsent
          label: Sign me up to recieve my words
          isRequired: false
          width: full
          type: CheckboxFormControl
      submitLabel: "Submit 🚀"
      styles:
        self:
          textAlign: center
    styles:
      self:
        height: auto
        width: narrow
        margin:
          - mt-0
          - mb-0
          - ml-4
          - mr-4
        padding:
          - pt-12
          - pb-12
          - pr-4
          - pl-4
        flexDirection: row
        textAlign: left
---