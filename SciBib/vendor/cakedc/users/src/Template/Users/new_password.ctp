<div class="users form">
    <?= $this->Flash->render('auth') ?>
    <?= $this->Form->create($user) ?>
    <fieldset>
        <legend><?= __d('Users', 'Please enter the password for your new user') ?></legend>
        <?= $this->Form->input('password'); ?>
        <?= $this->Form->input('password_confirm', ['type' => 'password', 'required' => true]); ?>

    </fieldset>
    <?= $this->Form->button(__d('Users', 'Submit')); ?>
    <?= $this->Form->end() ?>
</div>