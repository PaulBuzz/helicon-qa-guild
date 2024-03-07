import { Selector } from 'testcafe';

fixture `Zeus Test Stage`
    .page `https://zeus.stage.intfas.se/admin/login/?next=/admin/`;

test('Check value stage', async t => {
    await t
        .typeText('[name="username"]', 'pavel')
        .pressKey('tab')
        .typeText('[name="password"]', 'hello1pavel!')
        .click('[type="submit"]');
    
    await t.click(Selector('a').withText('VIEW SITE'));
    await t.expect(Selector('h1').innerText).contains('C1');
    await t.expect(t.eval(() => window.location.href)).eql('https://zeus.stage.intfas.se/api/cluster/cluster-activities/');

    const socParagraph = Selector('p').withText('SoC:');
    const socText = await socParagraph.innerText;
    const socValue = parseFloat(socText.split(':')[1].replace('%', '').trim());
    const formattedSoCValue = socValue.toFixed(1);

    console.log(`Type of SoC value: ${typeof socValue}`);
    console.log(`SoC value: ${formattedSoCValue}`);

    await t.expect(typeof socValue).eql('number');
    console.log('Check 1: Type of socValue is a number');

    await t.expect(formattedSoCValue).eql('NaN');
    console.log('Check 2: Formatted SoC value is NaN');
});

fixture `Zeus Test Local`
    .page `http://127.0.0.1:8000/admin/login/?next=/admin/`

test('Check value local', async t => {
    await t
        .typeText('[name="username"]', 'admin')
        .pressKey('tab')
        .typeText('[name="password"]', 'password')
        .click('[type="submit"]');
    
    await t.click(Selector('a').withText('VIEW SITE'));
    await t.expect(Selector('h1').innerText).contains('ADS-TEC');
    await t.expect(t.eval(() => window.location.href)).eql('http://127.0.0.1:8000/api/cluster/cluster-activities/');

    const socParagraph = Selector('p').withText('SoC:');
    const socText = await socParagraph.innerText;
    const socValue = parseFloat(socText.split(':')[1].replace('%', '').trim());
    const formattedSoCValue = socValue.toFixed(1);

    console.log(`Type of SoC value: ${typeof socValue}`);
    console.log(`SoC value: ${formattedSoCValue}`);

    await t.expect(typeof socValue).eql('number');
    console.log('Check 1: Type of socValue is a number');

    await t.expect(formattedSoCValue).eql('50.0');
    console.log('Check 2: Formatted SoC value is NaN');
});